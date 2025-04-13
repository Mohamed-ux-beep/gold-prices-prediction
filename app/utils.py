import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import subprocess
from omegaconf import OmegaConf

CONFIG_PATH = "config/config.yaml"


def fetch_gold_price():
    url = "https://www.goldpreis.de/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span", class_="au_gold_eur_o")
        if price_span:
            price_text = price_span.text.strip().replace(".", "").replace(",", ".")
            return float(price_text)
    except Exception as e:
        print(f"❌ Error fetching price: {e}")
    return None


def save_to_csv(timestamp, price):
    config = OmegaConf.load(CONFIG_PATH)
    data_path = config.paths.data
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    file_exists = os.path.isfile(data_path)

    with open(data_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "price_eur"])
        writer.writerow([timestamp, price])

    # Train model if data has 1000 rows
    try:
        df = pd.read_csv(data_path)
        if len(df) == 1000:
            print("📈 Data reached 1000 rows. Triggering model training...")
            date_str = datetime.now().strftime("%Y%m%d")
            model_name = f"xgboost_{date_str}.pkl"
            os.environ["MODEL_NAME_OVERRIDE"] = model_name  # pass to training script
            subprocess.run(["python", "app/training.py"], check=True)
    except Exception as e:
        print(f"❌ Error checking data size or triggering training: {e}")


def load_price_data():
    config = OmegaConf.load(CONFIG_PATH)
    data_path = config.paths.data
    if not os.path.exists(data_path):
        return []
    with open(data_path, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

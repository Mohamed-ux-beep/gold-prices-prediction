import os
import requests
from bs4 import BeautifulSoup
import json
import time
from kafka import KafkaProducer
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

# Read the Kafka broker from environment variable, default to 'localhost:9092' if not set
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

def create_producer():
    while True:
        try:
            print(f"⏳ Trying to connect to Kafka at {KAFKA_BROKER}...", flush=True)
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Connected to Kafka.", flush=True)
            return producer
        except Exception as e:
            print(f"❌ Kafka not ready, retrying in 5s... ({e})", flush=True)
            time.sleep(5)

producer = create_producer()

def fetch_gold_price():
    url = "https://www.goldpreis.de/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span", class_="au_gold_eur_o")

        if price_span:
            price_text = price_span.text.strip().replace(".", "").replace(",", ".")
            print(f"💰 Fetched gold price: {price_text} EUR", flush=True)
            return float(price_text)
    except Exception as e:
        print(f"❌ Error fetching gold price: {e}", flush=True)

    return None

@app.get("/")
def root():
    return {"status": "Gold price producer is running 🚀"}

@app.post("/send-price")
def send_price():
    price = fetch_gold_price()
    if price:
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "price_eur": price
        }
        try:
            producer.send("gold_prices_eur", message)
            producer.flush()
            print(f"✅ Sent price: {price} EUR at {message['timestamp']}", flush=True)
            return {"status": "sent", "data": message}
        except Exception as e:
            print(f"❌ Failed to send message to Kafka: {e}", flush=True)
            return {"status": "failed", "error": str(e)}
    return {"status": "no_price"}



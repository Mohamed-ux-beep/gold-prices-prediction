import requests
from datetime import datetime
import json
import time
from bs4 import BeautifulSoup

while True:
    try:
        response = requests.get("https://www.goldpreis.de/", headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span", class_="au_gold_eur_o")
        if price_span:
            price_text = price_span.text.strip().replace(".", "").replace(",", ".")
            price = float(price_text)
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "price_eur": price
            }
            requests.post(
                "https://<your-app>.up.railway.app/send-price",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data)
            )
            print("✅ Sent:", data)
    except Exception as e:
        print("❌ Error:", e)
    time.sleep(300)  # every 5 minutes


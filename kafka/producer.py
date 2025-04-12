import requests 
from bs4 import BeautifulSoup
import json 
import time 
from kafka import KafkaProducer 
from datetime import datetime 

def create_producer():
    while True:
        try:
            print("⏳ Trying to connect to Kafka...", flush=True)
            producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer= lambda v: json.dumps(v).encode('utf-8'))
            print("✅ Connected to Kafka.", flush=True)
            return producer
        except Exception as e:
            print(f"❌ Kafka not ready, retrying in 5s... ({e})", flush=True)
            time.sleep(5)



def fetch_gold_price():
    url = "https://www.goldpreis.de/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span",  class_ = "au_gold_eur_o")
        
        if price_span: 
            price_text = price_span.text.strip().replace(".", "").replace(",",".")
            print(f"💰 Fetched gold price: {price_text} EUR", flush=True)
            return float(price_text)
    except Exception as e:
        print(f"❌ Error fetching gold price: {e}", flush=True)

    return None

producer = create_producer()

while True:
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
        except Exception as e:
            print(f"❌ Failed to send message to Kafka: {e}", flush=True)

    # each 5 minutes send the value 
    print("⏳ Sleeping for 5 minutes...", flush=True)
    time.sleep(300)

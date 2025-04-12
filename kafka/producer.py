import requests 
from bs4 import BeautifulSoup
import json 
import time 
from kafka import KafkaProducer 
from datetime import datetime 

def create_producer():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer= lambda v: json.dumps(v).encode('utf-8'))
            print("✅ Connected to Kafka.")
            return producer
         except Exception as e:
             print(f"❌ Kafka not ready, retrying in 5s... ({e})")
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
            return float(price_text)
    except:
        return None

    return None

while True:
    producer = create_producer()
    price = fetch_gold_price()
    if price:
        message = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "price_eur": price
                }
        producer.send("gold_prices_eur", message)
        producer.flush()

    # each 5 minutes send the value 
    time.sleep(300)

from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import time

app = FastAPI()

class PriceData(BaseModel):
    timestamp: str
    price_eur: float

# ✅ Create KafkaProducer only when needed
def get_kafka_producer(retries=5, delay=5):
    for _ in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Kafka connected")
            return producer
        except Exception as e:
            print(f"❌ Kafka not ready: {e}")
            time.sleep(delay)
    return None

@app.get("/")
def health_check():
    return {"status": "✅ FastAPI is running"}

@app.post("/send-price")
async def send_price(data: PriceData):
    producer = get_kafka_producer()
    if not producer:
        return {"status": "❌ Kafka connection failed"}

    try:
        message = data.dict()
        producer.send("gold_prices_eur", value=message)
        producer.flush()
        return {"status": "✅ Sent to Kafka", "data": message}
    except Exception as e:
        return {"status": "❌ Kafka error", "error": str(e)}


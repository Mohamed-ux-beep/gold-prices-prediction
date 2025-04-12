from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json, time

app = FastAPI()

class PriceData(BaseModel):
    timestamp: str
    price_eur: float

# Try to connect to Kafka broker with retry
def get_kafka_producer():
    for attempt in range(5):
        try:
            print("🔁 Attempting to connect to Kafka...", flush=True)
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Connected to Kafka", flush=True)
            return producer
        except Exception as e:
            print(f"❌ Kafka not ready: {e}", flush=True)
            time.sleep(5)
    print("❌ Failed to connect to Kafka after retries", flush=True)
    return None

@app.post("/send-price")
async def send_price(data: PriceData):
    producer = get_kafka_producer()
    if not producer:
        return {"status": "❌ Kafka connection failed. Try again later."}

    message = data.dict()
    try:
        producer.send("gold_prices_eur", value=message)
        producer.flush()
        return {"status": "✅ Sent to Kafka", "data": message}
    except Exception as e:
        return {"status": "❌ Failed to send to Kafka", "error": str(e)}


from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json

app = FastAPI()

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Expected data model from POST
class PriceData(BaseModel):
    timestamp: str
    price_eur: float

@app.post("/send-price")
async def send_price(data: PriceData):
    message = data.dict()
    try:
        producer.send("gold_prices_eur", value=message)
        producer.flush()
        print(f"✅ Sent to Kafka: {message}", flush=True)
        return {"status": "✅ Sent to Kafka", "data": message}
    except Exception as e:
        print(f"❌ Error sending to Kafka: {e}", flush=True)
        return {"status": "❌ Failed to send", "error": str(e)}


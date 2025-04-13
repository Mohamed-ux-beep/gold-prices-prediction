from fastapi import FastAPI
from datetime import datetime, timezone
from app.utils import fetch_gold_price, save_to_csv, load_price_data
from app.model import load_model, predict_price
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Gold price app is running 🚀"}

@app.post("/send-price")
def send_price():
    price = fetch_gold_price()
    if price:
        timestamp = datetime.now(timezone.utc).isoformat()
        save_to_csv(timestamp, price)
        return {"status": "saved", "timestamp": timestamp, "price_eur": price}
    return {"status": "error", "message": "Failed to fetch price"}

@app.get("/predict")
def get_prediction():
    model = load_model()
    data = load_price_data()
    if not data:
        return {"status": "error", "message": "No data available"}
    prediction = predict_price(model, data)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prediction": prediction
    }

@app.get("/chart", response_class=HTMLResponse)
def plot_chart():
    data = load_price_data()
    if not data:
        return "<h2>No data available</h2>"

    timestamps = [row["timestamp"] for row in data]
    prices = [row["price_eur"] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices, marker='o', linestyle='-', color='gold')
    plt.title("Gold Price Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Price (EUR)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return f"""
        <html>
        <head><title>Gold Price Chart</title></head>
        <body>
            <h2>Gold Price Over Time</h2>
            <img src='data:image/png;base64,{img_base64}'/>
        </body>
        </html>
    """

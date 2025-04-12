# 📈 Gold Price Prediction Pipeline

This project provides a fully automated pipeline for scraping real-time gold prices, publishing them to Kafka, and optionally predicting future prices using a machine learning model. It's built with Python, Kafka, Docker, and integrated with GitLab CI/CD for continuous execution.

## 🚀 Features

- Scrapes live gold price from trusted websites
- Sends price data to a Kafka topic every 5 minutes
- Automatically runs via GitLab CI/CD pipeline
- Ready for deployment using Docker or on cloud platforms
- Supports cloudflared/ngrok for public Kafka access
- Flexible to integrate prediction, monitoring, and retraining

## 🛠 Technologies

- Python 3.11
- Apache Kafka & Zookeeper
- Kafka UI (for inspecting topics)
- BeautifulSoup + Requests
- GitLab CI/CD
- Docker & docker-compose
- (Optional) Prometheus, Grafana, n8n

## ⚙️ How to Run Everything Locally (One Cell)

```bash
# ✅ 1. Clone the project
git clone https://gitlab.com/your-username/gold-price-prediction.git
cd gold-price-prediction

# ✅ 2. Start Kafka, Zookeeper, and Kafka UI
docker-compose down
docker-compose up -d

# ✅ 3. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# ✅ 4. Install Python dependencies
pip install -r requirements.txt

# ✅ 5. Run the Kafka producer (scraper)
python kafka/producer.py
```

## ☁️ Running with GitLab CI/CD

1. Push your project to GitLab  
2. Make sure `.gitlab-ci.yml` is in the project root  
3. Go to **CI/CD → Schedules** and add a new schedule:  
   - Cron: `*/5 * * * *`  
   - Branch: `main`  
4. Your scraper will now run automatically every 5 minutes

✅ Make sure Kafka is accessible from GitLab (via public IP, cloudflared, or Confluent Cloud).

## 🌐 Kafka Access Options

To allow the GitLab runner to send messages to Kafka, use one of the following:

- [Cloudflared](https://developers.cloudflare.com/cloudflared/) tunnel to expose `localhost:9092`
- [Confluent Cloud](https://confluent.io) – free managed Kafka service
- Deploy your Kafka broker to Render, Railway, or any public cloud VM

## ✅ Next Steps (Optional Ideas)

- Add consumer logic and ML model for forecasting  
- Train model automatically on latest data  
- Add FastAPI service for real-time predictions  
- Monitor data & model metrics using Grafana + Prometheus  
- Automate workflows using n8n

## 📄 License

This project is intended for educational and research use. Contributions are welcome!


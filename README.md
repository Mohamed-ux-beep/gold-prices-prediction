```markdown
# Gold Price Prediction 📈

This project is a **complete end-to-end machine learning pipeline** for real-time **gold price prediction**. It integrates **web scraping**, **data storage**, **ML model training**, **prediction serving**, and **visualization**, all deployed to the cloud and **automated for 24/7 operation**.

---

## 🔧 Features

- ✅ **FastAPI backend** deployed via **Railway**  
- 🔁 **GitHub Actions** scheduled job scrapes gold prices every 5 minutes from [goldpreis.de](https://www.goldpreis.de)  
- 🧠 **Scikit-learn** model predicts future gold prices  
- 🗂️ **CSV-based historical data** storage  
- 📊 Interactive **price chart** served via API  
- 🔮 **Live prediction** with `/predict` endpoint  

---

## 📁 Project Structure

```
gold-price-prediction/
├── app/
│   ├── main.py             # FastAPI API
│   ├── model.py            # Prediction logic
│   ├── training.py         # Model training script
│   ├── utils.py            # Scraper and utility functions
│   └── run_scraper.py      # Script to run scraper + training
├── configs/
│   └── config.yaml         # Configuration file
├── dashboard/
│   ├── __init__.py         # Dashboard package init
│   └── app.py              # Optional dashboard frontend
├── data/
│   └── gold_prices.csv     # Historical gold price data
├── models/
│   └── model.pkl           # Trained ML model
├── .github/
│   └── workflows/
│       └── scrape_and_train.yml  # GitHub Actions workflow
├── requirements.txt
├── Procfile                # For Railway deployment
└── README.md
```

---

## 🚀 Deployment

- **Backend**: Deployed with Railway using `Procfile`  
- **Scheduler**: GitHub Actions (`scrape_and_train.yml`) runs scraping + training every 5 minutes  

---

## 🧠 Training the Model

To train the model manually:

```bash
python app/training.py
```

- Reads historical data from `data/gold_prices.csv`  
- Trains and saves model to `models/model.pkl`  

---

## 🔌 API Endpoints

| Endpoint       | Method | Description                          |
|----------------|--------|--------------------------------------|
| `/`            | GET    | Service health/status check          |
| `/send-price`  | POST   | Scrapes and stores latest gold price |
| `/predict`     | GET    | Predicts the next gold price         |
| `/chart`       | GET    | Displays interactive price history   |

---

## 🧪 Example Prediction Response

```json
{
  "timestamp": "2025-04-13T10:00:00Z",
  "price_eur": 2850.27,
  "prediction": 2861.45
}
```

---

## 🤖 GitHub Actions Workflow

**Path**: `.github/workflows/scrape_and_train.yml`

- 🕐 Runs every 5 minutes  
- 🌐 Scrapes the current gold price  
- 🧠 Triggers model training  
- 📬 Sends data to the `/send-price` endpoint  

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🙌 Contributors

Built with ❤️ by:

- **Mohamed Abokahf**  
- **Mohamed Sayed Noureldih Elsayed**  
- **Ferass Alrawashdh**

---
```


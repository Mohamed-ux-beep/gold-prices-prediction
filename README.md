# project description

# Gold Price Prediction 📈

This project is a complete end-to-end machine learning system for predicting gold prices. It combines scraping, data storage, model training, prediction serving, and visualization — all deployed to the cloud and automated for 24/7 operation.

## 🔧 Features
- ✅ **FastAPI** backend deployed on Railway
- 🔁 **GitHub Actions** job runs every 5 minutes to scrape gold price from [goldpreis.de](https://www.goldpreis.de)
- 🧠 **Scikit-learn model** for predicting future gold prices
- 🗂️ **CSV file** stores historical price data
- 📊 **Interactive chart** endpoint for visualization
- 🔮 `/predict` endpoint for live model inference

## 📁 Project Structure
```
gold-price-prediction/
├── app/
│   ├── main.py          # FastAPI API
│   ├── model.py         # Prediction logic
│   ├── training.py      # Model training
│   └── utils.py         # Scraping and helpers
├── data/
│   └── gold_prices.csv  # Saved scraped data
├── models/
│   └── model.pkl        # Trained model
├── .github/workflows/
│   └── scraper.yml      # GitHub Action: scrape & send price
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🚀 Deployment
- Backend: Railway (uses `Dockerfile` to deploy FastAPI app)
- Scheduled Jobs: GitHub Actions (`scraper.yml`)

## 🧠 Training the Model
To train the model manually:
```bash
python app/training.py
```
This script reads from `data/gold_prices.csv`, trains a model, and saves it to `models/model.pkl`.

## 🔌 API Endpoints
| Endpoint       | Method | Description                             |
|----------------|--------|-----------------------------------------|
| `/`            | GET    | Service status                          |
| `/send-price`  | POST   | Scrapes & stores gold price             |
| `/predict`     | GET    | Returns the predicted next price        |
| `/chart`       | GET    | Displays a plot of price history        |

## 🧪 Example Response
```json
{
  "timestamp": "2025-04-13T10:00:00Z",
  "price_eur": 2850.27,
  "prediction": 2861.45
}
```

## 🤖 GitHub Action Workflow
Located in `.github/workflows/scraper.yml` — it:
- Runs every 5 minutes
- Scrapes gold price
- Sends it to `/send-price`

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

## 🙌 Credits
Built with ❤️ using FastAPI, scikit-learn, GitHub Actions, Railway.

---
> Ready to scale up with real-time ML workflows and 24/7 deployment!


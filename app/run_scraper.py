from utils import fetch_gold_price, save_to_csv
from datetime import datetime

price = fetch_gold_price()
if price:
    save_to_csv(datetime.utcnow().isoformat(), price)
else:
    print('❌ No price fetched')


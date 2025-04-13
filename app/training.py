# app/training.py

import os
import numpy as np
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from hydra import main
from omegaconf import DictConfig
from datetime import datetime


def load_training_data(data_path):
    df = pd.read_csv(data_path)
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["price_eur"].values
    return X, y


@main(config_path="../config", config_name="config")
def train_all_models(cfg: DictConfig):
    model_dir = cfg.paths.models
    os.makedirs(model_dir, exist_ok=True)
    X, y = load_training_data(cfg.paths.data)

    for model_cfg in cfg.models:
        name = model_cfg.name
        mtype = model_cfg.type

        # if MODEL_NAME_OVERRIDE is set, use that instead of the config name (only for first model)
        if os.environ.get("MODEL_NAME_OVERRIDE") and model_cfg == cfg.models[0]:
            name = os.environ["MODEL_NAME_OVERRIDE"].replace(".pkl", "")

        if mtype == "xgboost":
            dtrain = xgb.DMatrix(X, label=y)
            params = {"objective": "reg:squarederror"}
            model = xgb.train(params, dtrain, num_boost_round=50)
        elif mtype == "linear":
            model = LinearRegression()
            model.fit(X, y)
        else:
            print(f"⚠️ Unknown model type: {mtype}")
            continue

        path = os.path.join(model_dir, f"{name}.pkl")
        joblib.dump(model, path)
        print(f"✅ Trained and saved: {name} → {path}")


if __name__ == "__main__":
    train_all_models()


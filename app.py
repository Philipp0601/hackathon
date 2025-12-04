# app.py
import os
import numpy as np
import xgboost as xgb
from fastapi import FastAPI
from pydantic import BaseModel

# Pfad zum Modell im Container
MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.json")

# XGBoost-Booster laden
bst = xgb.Booster()
bst.load_model(MODEL_PATH)

app = FastAPI()

class PredictRequest(BaseModel):
    # Eine Liste von Samples, jedes Sample = Feature-Liste
    features: list[list[float]]

class PredictResponse(BaseModel):
    predictions: list[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    X = np.array(req.features, dtype=float)
    dmatrix = xgb.DMatrix(X)
    preds = bst.predict(dmatrix)
    return PredictResponse(predictions=preds.tolist())

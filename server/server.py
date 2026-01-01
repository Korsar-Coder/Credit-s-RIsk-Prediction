import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
from functools import cache

app = FastAPI()
    
class Features(BaseModel):
    salary: float
    int_rate: float
    loan: float
    other_loans: int
    home_status: str
    purpose: str

@cache
def get_min_values(): return pd.read_csv("../Data/min_vals", dtype= float).values.tolist()
@cache
def get_max_values(): return pd.read_csv("../Data/max_vals", dtype= float).values.tolist()

def normalize_features(features: list):
    min = get_min_values()
    max = get_max_values()
    last_col_to_normalize = 3
    for key, (min_val, max_val) in enumerate(zip(min, max, strict=True)):
        min_val, max_val = min_val[0], max_val[0]
        features[key] = (features[key] - min_val) / (max_val - min_val)
        if key == last_col_to_normalize:
            break
    return np.reshape(features, shape = (1, -1))
@cache
def load_random_forest():
    path = "../RandomForest.sav"
    return load(path)

model = load_random_forest()

@app.post("/Predict")
def predict(features: Features):
    features = list(features)
    for index, (name, value) in enumerate(features):
        features[index] = value
    answer = [1]
    return {"Одобрено!" if answer == [0] else "Вы ненадежный!"}
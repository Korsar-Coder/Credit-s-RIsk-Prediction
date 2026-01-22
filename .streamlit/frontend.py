import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from os.path import join

pd.set_option("display.float_format", lambda x: "%0.3f" % x)
np.set_printoptions(suppress=True)

@st.cache_data
def get_min_values(): return pd.read_csv("../Data/min_vals", dtype= float).values.tolist()

@st.cache_data
def get_max_values(): return pd.read_csv("../Data/max_vals", dtype= float).values.tolist()

def normalize_features(features: list):
    min = get_min_values()
    max = get_max_values()
    last_col_to_normalize = 2
    for key, (min_val, max_val) in enumerate(zip(min, max, strict=True)):
        min_val, max_val = min_val[0], max_val[0]
        features[key] = (features[key] - min_val) / (max_val - min_val)
        if key == last_col_to_normalize:
            break
    return np.reshape(features, shape = (1, -1))

@st.cache_resource
def load_model(model_name: str):
    models_path = "../models"
    path = join(models_path, model_name + ".sav").replace("\\", "/")
    print(path)
    return load(path)


home_states = {1:"Сьемная квартира", 2: "Ипотека", 3: "Полностью владеете", 4:"Другое"}
purposes = {1: "Погасить задолжность", 2: "Купить авто", 3: "Оформляю кредитную карту", 
                4:"На новое жилье", 5: "Большая покупка", 5: "Предпринимательство", 6: "Отпуск",
                7: "Другое"}

st.title("Приветствуем вас на странице одобрения кредита!", text_alignment="center")
loan = st.slider("Сумма кредита (тыс)", 5, 3000, value= 100, step=5) * 1000
int_rate = st.slider("Процентная ставка", 5, 24, 15) / 100
salary = st.slider("Ваша ежемесячная зарплата (тыс)", 5, 1_000, 100, step=10) * 1000
home_status = st.selectbox("В каком состоянии ваше жилье?",
              options=home_states.values())
purpose = st.selectbox("Для чего вы берете кредит?",
             options=purposes.values())
features = [salary, int_rate, loan, 1 if home_status == "Ипотека" else 0,
                    1 if home_status == "Другое" else 0, 
                    1 if home_status == "Полностью владеете" else 0,
                    1 if home_status == "Сьемная квартира" else 0,
                    1 if purpose == "Погасить задолжность" else 0, 
                    1 if purpose == "Купить авто" else 0,
                    1 if purpose == "Оформляю кредитную карту" else 0, 
                    1 if purpose == "На новое жилье" else 0,
                    1 if purpose == "Большая покупка" else 0, 
                    1 if purpose == "Другое" else 0,
                    1 if purpose == "Предпринимательство" else 0, 
                    1 if purpose == "Отпуск" else 0]
choosed_model = st.sidebar.selectbox("Какую модель использовать?", options=["LogisticRegression", "RandomForest"], 
                             index = 1)
model = load_model(choosed_model)
print(features)
if choosed_model != "RandomForest":
   features = normalize_features(features)
else:
    features = np.reshape(features, (1,-1))

answer = model.predict(features)

st.write(answer)
print(features)
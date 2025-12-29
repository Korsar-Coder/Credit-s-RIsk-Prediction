import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

@st.cache_data
def get_min_values(): return pd.read_csv("../Data/min_vals", dtype= float).values.tolist()

@st.cache_data
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

@st.cache_resource
def load_random_forest():
    path = "../RandomForest.sav"
    return load(path)

model = load_random_forest()
home_states = {1:"Сьемная квартира", 2: "Ипотека", 3: "Полностью владеете", 4:"Другое"}
purposes = {1: "Погасить задолжность", 2: "Купить авто", 3: "Оформляю кредитную карту", 
                4:"На новое жилье", 5: "Большая покупка", 5: "Предпринимательство", 6: "Отпуск",
                7: "Другое"}

st.title("Приветствуем вас на странице одобрения кредита!", text_alignment="center")
loan = st.slider("Сумма кредита", 5000, 1_000_000, value= 200_000, step=5_000)
int_rate = st.slider("Процентная ставка", 5, 30, 15)
salary = st.slider("Ваша ежемесячная зарплата", 5000, 500_000, 100_000)
other_loans = st.slider("Сколько еще у вас кредитов?", 0, 40, 10)
home_status = st.selectbox("В каком состоянии ваше жилье?",
              options=["Аренда", "Ипотека", "Полностью оплачено", "Иное"])
purpose = st.selectbox("Для чего вы берете кредит?",
             options=purposes.values())
features = [salary, int_rate, loan, other_loans, 1 if home_status == "Ипотека" else 0,
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
features = normalize_features(features)
answer = model.predict(features)
st.write(answer)
import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from os.path import join

pd.set_option("display.float_format", lambda x: "%0.3f" % x)
np.set_printoptions(suppress=True)

@st.cache_resource
def load_model(model_name: str):
    models_path = "models"
    path = join(models_path, model_name + ".pkl").replace("\\", "/")
    print(path)
    return load(path)


home_states = ["Сьемная квартира","Ипотека", "Полностью владеете", "Другое"]
purposes = ["Погасить задолжность", "Купить авто", "Оформляю кредитную карту", 
                "На новое жилье","Большая покупка", "Предпринимательство", "Отпуск",
            "Другое"]

with st.form("Приветствуем вас на странице одобрения кредита!"):
    loan = st.slider("Сумма кредита (тыс)", 5, 3000, value= 100, step=5) * 1000
    int_rate = st.slider("Процентная ставка", 5, 30, 15) / 100
    salary = st.slider("Ваша ежемесячная зарплата (тыс)", 5, 1_000, 100, step=10) * 1000 * 12
    home_status = st.selectbox("В каком состоянии ваше жилье?",
                options=home_states)
    purpose = st.selectbox("Для чего вы берете кредит?",
                options=purposes)
    features = pd.DataFrame(data={
        "annual_income_ru":[salary],
        "loan_ammount_ru":[loan],
        "int_rate_ru":[int_rate],
        "home_ownership":[home_status],
        "purpose":[purpose]
    })
    # choosed_model = st.sidebar.selectbox("Какую модель использовать?", options=["LogisticRegression", "RandomForest"], 
    #                             index = 1)
    choosed_model = "LogisticRegression"
    submitted = st.form_submit_button(label="Оценить заявку")

if submitted:
    model = load_model(choosed_model)
    # if choosed_model != "RandomForest":
    #     features = normalize_features(features)
    # else:
    #     features = np.reshape(features, (1,-1))
    answer = model.predict(features)
    if answer == 0:
        st.success("Одобрено!")
    else:
        st.error("Вы ненадежный!")
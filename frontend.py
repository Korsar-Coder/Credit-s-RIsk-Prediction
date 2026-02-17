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
    extension = ".joblib"
    path = join(models_path, model_name + extension).replace("\\", "/")
    print(path)
    return load(path)

def predict_bayes(components: dict,features: pd.DataFrame) -> tuple:
    scaler = components['scaler']
    numeric_cols = components["numeric_cols"]
    categorical_cols = components["categorical_cols"]
    encoder = components['encoder']
    gnb = components['gnb']
    bern = components['bern']
    ensemble = components['ensemble']
    threshold = ensemble.best_threshold_

    X_num = features[numeric_cols].values  
    X_cat = features[categorical_cols].values
    X_num_scaled = scaler.transform(X_num)
    X_cat_encoded = encoder.transform(X_cat)

    gnb_proba = gnb.predict_proba(X_num_scaled)[:, 1]
    bern_proba = bern.predict_proba(X_cat_encoded)[:, 1]

    X_meta = np.column_stack([gnb_proba, bern_proba])

    prediction = ensemble.predict_proba(X_meta)
    final_proba = prediction[:,1][0]
    answer = 1 if final_proba >= threshold else 0
    print(prediction)
    return (answer, final_proba)

home_states = ["Сьемная квартира","Ипотека", "Полностью владеете", "Другое"]
purposes = ["Погасить задолжность", "Купить авто", "Оформляю кредитную карту", 
                "На новое жилье","Большая покупка", "Предпринимательство", "Отпуск",
            "Другое"]

purpose_converter = {"Погасить задолжность":"Debt consolidation", "Другое":"other", "Купить авто":"car",
                    "Оформляю кредитную карту":"credit card", "Большая покупка":"major purchase",
                    "На новое жилье":"house", "Предпринимательство":"small business",
                    "Отпуск": "vacation"}
home_converter = {"Сьемная квартира": "RENT", "Ипотека":"MORTGAGE", "Полностью владеете":"OWN", 
                  "Другое":"OTHER"}

st.title("Приветствуем вас на странице одобрения кредита!")
choosed_model = st.sidebar.selectbox("Какую модель использовать?", options=["LogisticRegression", "RandomForest",
                                                                            "NaiveBayes", "KNN"],  index = 0)
loan = st.slider("Сумма кредита (тыс)", 5, 3000, value= 100, step=5) * 1000
int_rate = st.slider("Процентная ставка", 5, 30, 15) / 100
salary = st.slider("Ваша ежемесячная зарплата (тыс)", 5, 1_000, 100, step=10) * 1000 * 12
home_status = st.selectbox("В каком состоянии ваше жилье?",
                options=home_states, disabled= True if choosed_model == "KNN" else False)
purpose = st.selectbox("Для чего вы берете кредит?",
                options=purposes, disabled= True if choosed_model == "KNN" else False)
DTI = loan / salary
features = pd.DataFrame(data={
        "annual_income_ru":[salary],
        "loan_ammount_ru":[loan],
        "int_rate_ru":[int_rate],
        "DTI":[DTI],
        "home_ownership":[home_converter.get(home_status)],
        "purpose":[purpose_converter.get(purpose)],
         })
features["purpose"] = features["purpose"].astype("category")
features["home_ownership"] = features["home_ownership"].astype("category")
print(features.info())

model = load_model(choosed_model)
if choosed_model == "NaiveBayes":
    answers = predict_bayes(model, features)
    answer = answers[0]
    proba = answers[1]
    proba = 1 - proba
else:
    answer = model.predict(features)
    proba = model.predict_proba(features)
    proba = str(proba[0]).partition(" ")[0][1:]
st.write("Надежность:")
st.progress(float(proba))
print(features)
if answer == 0:
    st.success("Одобрено!")
else:
    st.error("Вы ненадежный!")
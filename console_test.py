from joblib import load
import numpy as np
import pandas as pd

pd.set_option("display.float_format", lambda x: "%0.3f" % x)

def normalize_features(features: list):
    min = pd.read_csv("Data/min_vals", dtype= float).values.tolist()
    max = pd.read_csv("Data/max_vals", dtype= float).values.tolist()
    last_col_to_normalize = 3
    for key, (min_val, max_val) in enumerate(zip(min, max, strict=True)):
        min_val, max_val = min_val[0], max_val[0]
        features[key] = (features[key] - min_val) / (max_val - min_val)
        if key == last_col_to_normalize:
            break
    return np.reshape(features, shape = (1, -1))

def main():
    model_path = "RandomForest.sav"
    model = load(model_path)
    print("*" * 30 + " Создано ООО 'Кредитование у Дяди Вани' " + "*" * 30 + "\n")
    home_states = {1:"Сьемная квартира", 2: "Ипотека", 3: "Полностью владеете", 4:"Другое"}
    purposes = {1: "Погасить задолжность", 2: "Купить авто", 3: "Оформляю кредитную карту", 
                4:"На новое жилье", 5: "Большая покупка", 5: "Предпринимательство", 6: "Отпуск",
                7: "Другое"}
    while True:
        loan = float(input("На какую сумму берете кредит?: "))
        print("-" * 10)
        int_rate = float(input("Какова процентная ставка?: ")) / 100
        print("-" * 10)
        salary = float(input("Введите вашу ежемесячную ЗП, руб (все строго конфиденциально): "))
        print("-" * 10)
        other_loans = int(input("Сколько еще у вас кредитов? (Мы никому не сообщим): "))
        print("-" * 10)
        print("В каком состоянии ваше жилье? (Введите номер ответа):")
        for number, state in home_states.items():
            print(f"{number}: " + state)
        home_status = home_states.get(int(input("Номер ответа: ")), "Ипотека")
        print("-" * 10)
        print("Для чего вы берете кредит? (Введите номер ответа)")
        for number, purpose in purposes.items():
            print(f"{number}: " + purpose)
        purpose = purposes.get(int(input("Введите номер ответа: ")),"Оформляю кредитную карту")
        
        features = [salary, int_rate, loan, other_loans, 1 if home_status == "Ипотека" else 0,
                    1 if home_status == "Другое" else 0, 1 if home_status == "Полностью владеете" else 0,
                    1 if home_status == "Сьемная квартира" else 0,
                    1 if purpose == "Погасить задолжность" else 0, 1 if purpose == "Купить авто" else 0,
                    1 if purpose == "Оформляю кредитную карту" else 0, 1 if purpose == "На новое жилье" else 0,
                    1 if purpose == "Большая покупка" else 0, 1 if purpose == "Другое" else 0,
                    1 if purpose == "Предпринимательство" else 0, 1 if purpose == "Отпуск" else 0]
        answer = model.predict(normalize_features(features))[0]
        print(answer)

main()
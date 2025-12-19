from joblib import load

def main():
    model_path = "KNN.sav"
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
        answer = model.predict([features])[0]
        print(answer)

if __name__ == "__main__": main()
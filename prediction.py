from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import requests
import pandas as pd
import datetime


class Predict:
    @staticmethod
    def currencies():
        df = pd.read_csv("file1.csv")
        return list(df['EngName'])

    @staticmethod
    def get_rcode(message):
        df = pd.read_csv('file1.csv', delimiter=',')
        df.drop('Unnamed: 0', axis=1)
        dfName = df.set_index('Name')
        dfEngName = df.set_index('EngName')
        try:
            return str(dfName.loc[message, 'Rcode'])[:6]
        except KeyError:
            try:
                return str(dfEngName.loc[message, 'Rcode'])[:6]
            except KeyError:
                return "Нет такой валюты"

    def get_prediction(self, curr):
        today = datetime.datetime.today()
        tomorrow = (today + datetime.timedelta(days=1))
        df = self.get_period('01.01.2019', today, self.get_rcode(curr))  # с 2019 по текущее с rcode нужным
        new_row = {'date': [tomorrow], 'rate': [0]}
        new_df = pd.DataFrame(new_row)
        df = pd.concat([df, new_df])

        # разбиение даты на года\месяцы\недели
        df["weekday"] = df["date"].dt.weekday
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year
        df.drop(['date'], axis=1, inplace=True)

        # курсы за последние 7 дней (скроллинг\шифтинг)
        past_days = 7
        for day in range(past_days):
            d = day + 1
            df[f"curs_back_{d}d"] = df["rate"].shift(d)
        df.dropna(inplace=True)

        # бинарность столбцов по значениям
        df = pd.get_dummies(df, columns=["year", "month", "weekday"])

        # нужно создать последннюю строчку(как раз которую будем прогнозировать)
        # а именно входные данные, чтоб модели было на чём предсказывать
        new_df = df[-1:]
        df.drop(df.tail(1).index, inplace=True)

        # разметка на тестовые и тренировочные данные
        x = df.drop('rate', axis=1)
        y = df['rate']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

        # обучение
        model = LinearRegression()
        model.fit(x_train, y_train)

        # предсказание
        return round(model.predict(new_df.drop('rate', axis=1))[0], 3)

    @staticmethod
    def get_period(from_date, to_date, rcode):
        html = requests.get(
            f'https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ={rcode}&UniDbQuery.From={from_date}&UniDbQuery.To={to_date}').text
        table = ((pd.concat(pd.read_html(html), ignore_index=True)).drop(index=[0, 1])).reset_index(drop=True)
        table.columns = ['date', 'multiplier', 'rate']
        table['rate'], table['multiplier'] = pd.to_numeric(table['rate'], downcast="float"), pd.to_numeric(
            table['multiplier'])
        table['date'] = pd.to_datetime(table['date'], format="%d.%m.%Y")
        # for n in range(table.shape[0]):
        table['rate'] /= table['multiplier'] * 10000
        table = table.drop('multiplier', axis=1)
        table = table.iloc[::-1].reset_index(drop=True)
        return table

from datetime import datetime

import requests
import sqlite3


def save_currency_code_to_db(df, connection):
    cursor = connection.cursor()
    curr_code = cursor.execute("SELECT ID FROM CurrenciesTypes WHERE CurrencyCode = ?", [df['code']]).fetchall()
    if not curr_code:
        cursor.execute('''INSERT INTO CurrenciesTypes (CurrencyCode, CurrencyName) 
                        VALUES (?, ?)''', (df['code'], df['currency']))
        connection.commit()

def connect_to_db():
    connection = sqlite3.connect('waluty.db')
    cursor = connection.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS "CurrenciesTypes" (
                "Id"	INTEGER NOT NULL UNIQUE,
                "CurrencyName"	TEXT UNIQUE,
                "CurrencyCode"	TEXT UNIQUE,
                PRIMARY KEY("Id" AUTOINCREMENT)
            ) ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Rates" (
            "Id"	INTEGER NOT NULL UNIQUE,
            "EffectiveDate"	DATE,
            "Mid"	REAL,
            "CurrencyType"	INTEGER,
            FOREIGN KEY("CurrencyType") REFERENCES "CurrenciesTypes"("Id"),
            PRIMARY KEY("Id" AUTOINCREMENT)
        );''')
    connection.commit()

    return connection


def save_data_to_db(rates, connection, code):
    cursor = connection.cursor()
    curr_code = cursor.execute("SELECT ID FROM CurrenciesTypes WHERE CurrencyCode = ?", [code]).fetchone()[0]
    last_date_in_db = cursor.execute("SELECT max(EffectiveDate) FROM Rates WHERE currencyType = ?", [curr_code]).fetchone()[0]
    for rate in rates:
        if not last_date_in_db or datetime.strptime(rate['effectiveDate'], '%Y-%m-%d') > datetime.strptime(last_date_in_db, '%Y-%m-%d'):
            cursor.execute('''INSERT INTO Rates (EffectiveDate, Mid, CurrencyType)
                                 VALUES (?, ?, ?)''', (rate['effectiveDate'], rate['mid'], curr_code))

    connection.commit()


def main():
    currencies_codes = ['EUR', 'GBP', 'USD', 'CHF', 'JPY']
    connection = connect_to_db()
    for code in currencies_codes:
        response = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{code}/last/25/').json()
        save_currency_code_to_db(response, connection)
        save_data_to_db(response['rates'], connection, code)

if __name__ == "__main__":
    main()
import json
import requests
import time
import csv
import pandas as pd
import os

# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

# requesting data from url
data = requests.get(key)


def take_data():
    global data
    data = requests.get(key)
    data = data.json()
    count = 0
    with open("Coin_Prices.csv", "a", newline='') as coincsv:
        coin = csv.writer(coincsv)
        coin.writerow([data["price"]])
        # ,[data["price"]]

    print(f"{data['symbol']} fiyat : {data['price']}")


def check_prices():
    coinprices = pd.read_csv('sss.csv')
    print(coinprices)


# csvleri bu şekilde okuyalım pandas şaşırıyor.
rows = ['1', '2']
print(int(rows[0]))

with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Coin_Prices.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        r = row[0]
        print(float(r[2:]))
        rows.append(float(r)*float(r))
# okuduğum değerleri floata çeviriyorum int olmuyor malum uzun değerler olduğu için.
print(header)
print(type(rows))


# r = int(rows[5])
# print(int(rows[5]))
print(rows)

# print(int(rows[5])*int(rows[6]))

# PANDA İLE OKUMA
# coin_data = pd.read_csv(
#     'C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Coin_Prices.csv', encoding="utf-8", low_memory=False)


process_killer = 0
while True:

    time.sleep(0.2)
    take_data()

    if process_killer == 2:
        break

    process_killer += 1

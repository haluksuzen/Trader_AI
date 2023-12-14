import json
import requests
import time
import csv
import pandas as pd
import os

# Değişkenler
list_coindata = []
last_x_coindata = []

# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

# requesting data from url
data = requests.get(key)


def take_data():
    global data
    data = requests.get(key)
    data = data.json()
    count = 0
    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Coin_Prices.csv", "a", newline='') as coincsv:
        coin = csv.writer(coincsv)
        coin.writerow([data["price"]])
        print(data["price"])

# Trendin ne yönde olduğunu hesaplama


def create_last_x_coindata():
    counter = 0

    for i in list_coindata:
        counter += 1
        print(str(i) + "sdss" + str(len(list_coindata)))

        if counter > len(list_coindata) - 5:
            last_x_coindata.append(i)

    print(last_x_coindata)
    return last_x_coindata


def what_is_trend():
    print()


# '!!!!!' BOŞ VERİ OLUNCA CSV DE PATLIYOR
# Coin verilerinin anlık kaydedildiği csv dosyasını açıp, verileri dizi içerisine atıyorum
with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Coin_Prices.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        r = row[0]
        print(float(r[2:]))
        list_coindata.append(float(r))

print(list_coindata[5], create_last_x_coindata())

# ANA Döngü
process_killer = 0
while True:

    time.sleep(0.2)
    take_data()

    if process_killer == 2:
        break

    process_killer += 1

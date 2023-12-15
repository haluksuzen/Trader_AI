import json
import requests
import time
import csv
import pandas as pd
import os
import string
import random
from datetime import datetime

# Değişkenler
list_coindata = []
taked_coindata = []
last_x_coindata = []
_down = False
_float_Trend = False
_up = False
now = datetime.now()
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
        # print(data["price"])

# Random id oluşturma


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# son x datayı alıyor


def create_last_x_coindata():
    print(list_coindata[1])
    counter = 0

    for i in range(1, len(list_coindata)):
        counter += 1
        # print(str(i) + "sdss" + str(len(list_coindata)))

        if counter > len(list_coindata) - 5:
            last_x_coindata.append(list_coindata[i])

    return last_x_coindata

# trendin ne yönde olduğunu belileme


def what_is_trend(coin_dizi):
    print(last_x_coindata)
    counter = 0
    for i in range(1, len(coin_dizi)):
        if coin_dizi[i] < coin_dizi[i-1]:

            counter += 1

        if coin_dizi[i] >= coin_dizi[i-1]:

            counter -= 1
    # burayı test ettim doğru çalışıyor yüzde 66 ünden büyükse all şeklinde
    if counter >= (len(coin_dizi) - (len(coin_dizi)/3)):
        _down = True
        return _down
    # % x inden küçükse  düz devam ediyor
    if counter < (len(coin_dizi)/3):
        _float_Trend = True
        return _float_Trend
    # counter 0 dan küçükse yükseliş trendi var döndür
    if counter <= 0:
        _up = True
        return _up


def buy_sell():
    if _down and _float_Trend:  # _down and _float_Trend
        # detaylı bir şekilde alınan coin değerini not ediyoruz x boyutlu listeye
        with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Taked_Coin_Prices.csv", "a", newline='') as coincsv:
            coin = csv.writer(coincsv)
            coin.writerow([last_x_coindata[4], id_generator(),
                          now.strftime("%Y-%m-%d %H:%M:%S")])

    if _up:  # _up
        # alınan coin değerlerini çok boyutlu listeden okuyuoruz.
        with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Taked_Coin_Prices.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                r = row
                # print(float(r))
                # print(r)
                taked_coindata.append(r)
        # iki boyutluda istenilen datayı almak ***print(taked_coindata[5][1])
        for i in range(1, len(taked_coindata)):
            # taked_coindata[i][0] < last_x_coindata[4]
            if taked_coindata[i][0] < last_x_coindata[4]:
                with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Selled_Coin_Prices.csv", "a", newline='') as coincsv:
                    coin = csv.writer(coincsv)
                    coin.writerow([taked_coindata[i][0], taked_coindata[i][1], last_x_coindata[4],
                                   now.strftime("%Y-%m-%d %H:%M:%S")])


def list_Allcoin_data():
    # '!!!!!' BOŞ VERİ OLUNCA CSV DE PATLIYOR
    # Coin verilerinin anlık kaydedildiği csv dosyasını açıp, verileri dizi içerisine atıyorum
    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Coin_Prices.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            r = row[0]
            # print(float(r[2:]))
            list_coindata.append(float(r))


# ANA Döngü
process_killer = 0
while True:
    time.sleep(0.1)
    # take_data()
    list_Allcoin_data()
    create_last_x_coindata()
    what_is_trend(last_x_coindata)
    buy_sell()
    print(_up, _float_Trend, _down)
    print("Cycle : " + str(process_killer))

    # değişken resetleme
    last_x_coindata = []
    # ÇÖZMEM GEREKEN KISIM MNATIK HATASSSI OLAARK HEPSİ NEDEN FALSE OLUYOR.
    if process_killer == 5:
        break

    process_killer += 1

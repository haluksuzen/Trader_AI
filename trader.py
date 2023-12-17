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
selled_coindata = []
dont_sellinThis = []
_down = False
_float_Trend = False
_up = False
now = datetime.now()
son_kacData = 10
_cnt_takedCoinData = 0
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
# yüzde bulma


def percentage(percent, whole):
    return (percent * whole) / 100.0
# son x datayı alıyor


def create_last_x_coindata():
    # print(list_coindata[1])
    counter = 0

    for i in range(1, len(list_coindata)):
        counter += 1

        if counter > len(list_coindata) - son_kacData:
            last_x_coindata.append(list_coindata[i])

    return last_x_coindata

# trendin ne yönde olduğunu belileme


def what_is_trend(coin_dizi):
    counter_down = 0
    counter_float = 0
    counter_up = 0
    # dizinin ilk % x elemeanı düşüyorsa
    for i in range(1, int((percentage(50, len(coin_dizi))))):
        if coin_dizi[i] < coin_dizi[i-1]:
            counter_down += 1
            # print("düşüyor")
    # dizinin son x elemanı düşüyorsa
    for i in range(int((percentage(50, len(coin_dizi)))), len(coin_dizi)):
        if coin_dizi[i] >= coin_dizi[i-1]:
            counter_float += 1
            # print("düz gidiyor")
    # dizinin son x elemanı yükseliş trendindeyse
    for i in range(int((percentage(50, len(coin_dizi)))), len(coin_dizi)):
        if coin_dizi[i] > 0.2 + coin_dizi[i-1]:  # 0.5 +
            counter_up += 1

    # %xinden büyükse düşüş var
    if counter_down >= int((percentage(20, len(coin_dizi)))):
        global _down
        _down = True

    # % x inden büyükse  düz devam ediyor
    if counter_float >= int((percentage(20, len(coin_dizi)))):
        global _float_Trend
        _float_Trend = True

    # counter dizinin % xinden büyükse yükseliş trendi döndür
    if counter_up >= (percentage(20, len(coin_dizi))):
        global _up
        _up = True


def buy_sell():
    # alınan coin değerlerini çok boyutlu listeden okuyuoruz.
    # alınan coinlerin coountu olmalı yoksa döngüden dolayı patlıyor
    global _cnt_takedCoinData
    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Taked_Coin_Prices.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            r = row
            _cnt_takedCoinData += 1
            # print(float(r))
            # print(r)
            taked_coindata.append(r)

    if _down and _float_Trend:  # _down and _float_Trend
        yazabilir = True
        # detaylı bir şekilde alınan coin değerini not ediyoruz x boyutlu listeye
        with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Taked_Coin_Prices.csv", "a", newline='') as coincsv:
            coin = csv.writer(coincsv)
            # eğer alınan coinler halihazırda yeni coin ile eşleşiyorsa alma emri ver mükerrer olmasın
            for i in range(1, len(taked_coindata)):
                if int(float(taked_coindata[i][0])) == int(last_x_coindata[son_kacData-2]):
                    yazabilir = False

            if yazabilir:
                coin.writerow([last_x_coindata[son_kacData-2], id_generator(),
                               now.strftime("%Y-%m-%d %H:%M:%S")])

    if _up:  # _up
        # her seferinde tekrardan okumalıyız satılan coinleri
        read_SelledCoin_Prices()

        # iki boyutluda istenilen datayı almak ***print(taked_coindata[5][1])
        for i in range(1, _cnt_takedCoinData):
            # print(taked_coindata[i][1])
            # print(selled_coindata[son_kacData-2][1])
            # ALINanlar arasında şuadnaki coin verisinden düşük var ise bul
            if float(taked_coindata[i][0]) < last_x_coindata[son_kacData-2]:
                for j in range(1, len(selled_coindata)):
                    # düşük coin değeri daha önce satıldıysa ilgili id yi listeye ekle
                    if taked_coindata[i][1] == selled_coindata[j][1]:
                        dont_sellinThis.append(taked_coindata[i][1])

                # daha önce satılanlar listesinde yok ise satılanlara ekle
                if dont_sellinThis.count(taked_coindata[i][1]) == 0:
                    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Selled_Coin_Prices.csv", "a", newline='') as coincsv:
                        coin = csv.writer(coincsv)
                        coin.writerow([taked_coindata[i][0], taked_coindata[i][1], last_x_coindata[son_kacData-2],
                                       now.strftime("%Y-%m-%d %H:%M:%S")])


def read_SelledCoin_Prices():
    # satılanları oku
    global selled_coindata
    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Selled_Coin_Prices.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            r = row
            # print(float(r))
            # print(r)
            selled_coindata.append(r)


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


# Başlarken

process_killer = 0
print("Program Loading...")

# ANA Döngü
while True:
    time.sleep(10)
    take_data()
    list_Allcoin_data()
    create_last_x_coindata()
    what_is_trend(last_x_coindata)
    buy_sell()
    print(_up, _float_Trend, _down)
    print("Cycle : " + str(process_killer))

    # değişken resetleme
    _down = False
    _float_Trend = False
    _up = False
    last_x_coindata = []
    _cnt_takedCoinData = 0
    now = datetime.now()

    if process_killer == 18:
        break

    process_killer += 1
    # EN SON ALINANLARI SATARKENKİ SATIŞ FİYATINDA YANLIŞLIK VARDI

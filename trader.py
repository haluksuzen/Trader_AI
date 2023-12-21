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
son_kacData = 30
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
# verilen dizideki ilgili eleamnlardaki yüzdesel değişşim


def change_percentage(dizi, ilk_kac, son_kac):
    ilkler = []
    sonlar = []
    for i in range(1, ilk_kac):
        ilkler.append(dizi[i])
    for i in range(len(dizi) - son_kac, len(dizi)):
        sonlar.append(dizi[i])

    ilkorta = int(sum(ilkler)/len(ilkler))
    sonorta = int(sum(sonlar)/len(sonlar))

    return ilkorta, sonorta


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

    # dizinin ilk % x elemeanı düşüyorsa
    for i in range(1, int((percentage(40, len(coin_dizi))))):
        if coin_dizi[i] < coin_dizi[i-1]:
            counter_down += 1
            # print("düşüyor")
    # dizinin son x elemanı düşüyorsa
    for i in range(int((percentage(41, len(coin_dizi)))), int((percentage(80, len(coin_dizi))))):
        if coin_dizi[i] >= coin_dizi[i-1]:
            counter_float += 1
            # print("düz gidiyor")

    # %x aşağıda ise düşüş var
    if counter_down >= int((percentage(20, len(coin_dizi)))):
        global _down
        _down = True

    # % x inden büyükse  düz devam ediyor
    if counter_float >= int((percentage(20, len(coin_dizi)))):
        global _float_Trend
        _float_Trend = True


def buy_sell():
    # alınan coin değerlerini çok boyutlu listeden okuyuoruz.
    # alınan coinlerin coountu olmalı yoksa döngüden dolayı patlıyor
    global taked_coindata
    global _cnt_takedCoinData
    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Taked_Coin_Prices.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            r = row
            _cnt_takedCoinData += 1
            # print(float(r))
            # print(r)
            if taked_coindata.count(r) == 0:
                taked_coindata.append(r)

    if _down and _float_Trend:  # _down and _float_Trend
        yazabilir = True
        a, b = change_percentage(last_x_coindata, 10, 4)

        if (a - b) < (0.5*a/100):  # yüzde 2 sinden küçük ise düşüş
            yazabilir = False

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
                print("Taked...")
                print(last_x_coindata[son_kacData-2],
                      now.strftime("%Y-%m-%d %H:%M:%S"))

    if True:  # _up
        # DEĞİŞİKLİK -> ÖNCEDEN UP DOĞRU İSE SATIM YAPIYORDUK ŞİMDİ ALINANLARDA ŞUANKİ FİYATTAN DÜŞÜK VAR İSE
        # DİREK SATIYORUZ
        # her seferinde tekrardan okumalıyız satılan coinleri
        read_SelledCoin_Prices()

        global dont_sellinThis

        # iki boyutluda istenilen datayı almak ***print(taked_coindata[5][1])
        for i in range(1, _cnt_takedCoinData):
            # print(taked_coindata[i][1])
            # print(selled_coindata[son_kacData-2][1])
            # alınanlarda yüzde x den şimmdiki fiyattan düşük var ise sat

            if (float(last_x_coindata[son_kacData-2] - float(taked_coindata[i][0]))) >= 0.5*float(last_x_coindata[son_kacData-2])/100:
                for j in range(1, len(selled_coindata)):
                    # düşük coin değeri daha önce satıldıysa ilgili id yi listeye ekle
                    # if taked_coindata[i][1] == selled_coindata[j][1]: ---- BOŞ BU YANLIŞ KONTROL
                    # AMACIM SELLED DATA İN THİS GÜNCELLENDİĞİNDE DONT SELL İNTHİS GÜNCELLEMEK
                    # basit bir if ile şisme olmaması için var ise eklemiyoruz
                    if dont_sellinThis.count(selled_coindata[j][1]) == 0:
                        dont_sellinThis.append(selled_coindata[j][1])

                # daha önce satılanlar listesinde yok ise satılanlara ekle
                if dont_sellinThis.count(taked_coindata[i][1]) == 0:
                    with open("C:/Users/COMPUUTER5/Desktop/codinnngg/Python Programs/Trader_AI/Selled_Coin_Prices.csv", "a", newline='') as coincsv:
                        coin = csv.writer(coincsv)
                        coin.writerow([taked_coindata[i][0], taked_coindata[i][1], last_x_coindata[son_kacData-2],
                                       now.strftime("%Y-%m-%d %H:%M:%S")])
                        print("Selled...")
                        print([taked_coindata[i][0], taked_coindata[i][1], last_x_coindata[son_kacData-2],
                               now.strftime("%Y-%m-%d %H:%M:%S")])
                        print(round(100*(last_x_coindata[son_kacData-2] -
                              float(taked_coindata[i][0]))/last_x_coindata[son_kacData-2], 3), "Percentage Gain :)")


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

# LARI DİREK ELE ALABİLİRİM

# ANA Döngü
while True:
    time.sleep(120)
    take_data()
    list_Allcoin_data()
    create_last_x_coindata()
    what_is_trend(last_x_coindata)
    buy_sell()
    print(_float_Trend, _down)
    print("Cycle : " + str(process_killer))

    # değişken resetleme
    _down = False
    _float_Trend = False
    last_x_coindata = []
    dont_sellinThis = []
    taked_coindata = []

    _cnt_takedCoinData = 0
    now = datetime.now()

    if process_killer == 240:  # 7.5SAAT - 870
        break

    process_killer += 1

import csv
from datetime import datetime
from collections import defaultdict

#! PEMBUATAN ALGORITMA FUZZY TIME SERIES CHENG


def readcsv(filename):
    with open(filename,) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        data = []
        tanggal = []
        for row in readCSV:
            tanggal.append(row[1])
            data.append(row[2])
    return tanggal,data

def Prepocessing(data):
    strtanggal = data[0][1:]
    strharga = data[1][1:]
    exharga = [0]
    for i in range(len(strharga)):
        if strharga[i] == '-':
            strharga[i] = 0
    tanggal = [datetime.strptime(x,'%d/%m/%Y') for x in strtanggal]
    harga = list(map(int,strharga))
    minharga = min([x for x in harga if x not in exharga])
    maxharga = max([x for x in harga if x not in exharga])
    newminharga = minharga - 500
    newmaxharga = maxharga + 500
    namahari = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']
    for i in range(len(harga)):
        if harga[i] == 0:
            #* masukkan rumus preposessing data
            if namahari[tanggal[i].weekday()] in ['Sabtu','Minggu']:
                harga[i] = 0
                tanggal[i] = 0
            else:
                pre = (harga[i-1] - minharga) / (maxharga - minharga) * (newmaxharga-newminharga) + newminharga
                harga[i] = int(round(pre))
    tanggal = [x.date() for x in tanggal if x != 0]
    harga = [x for x in harga if x != 0]
    return tanggal,harga

def PlotMonth(dates,prices):
    #* Membuat kamus defaultdict untuk menyimpan harga-harga per bulan dan tahun
    prices_per_month_year = defaultdict(int)
    count_per_month_year = defaultdict(int)

    #* Mengelompokkan harga-harga per bulan dan tahun dan menghitung jumlah data per bulan dan tahun
    for date, price in zip(dates, prices):
        month_year = date.strftime('%Y-%m')
        prices_per_month_year[month_year] += price
        count_per_month_year[month_year] += 1

    #* Membuat array tanggal baru dan array harga baru
    new_dates = []
    new_prices = []

    #* Mengisi array tanggal baru dan array harga baru dengan nilai rata-rata per bulan dan tahun
    for month_year, price_sum in prices_per_month_year.items():
        count = count_per_month_year[month_year]
        average_price = price_sum / count
        new_dates.append(month_year)
        new_prices.append(int(round(average_price)))
    
    return new_dates,new_prices

def SemestaU(Data,D1,D2):
    #*masukkan rumus semesta U
    U = [min(Data) - D1 , max(Data) + D2]
    return U

def Mean(Data):
    #*masukkan rumus mean
    selisih = []
    for i in range(len(Data)):
        if i == len(Data)-1:
            break
        val = Data[i+1] - Data[i]
        selisih.append(abs(val))
    mean = sum(selisih)/(len(selisih)+1)
    return selisih,mean

def IntervalAVG(mean,semestaU):
    #* panjang interval
    lenInterval = mean/2
    #* l jumlah interval
    jumlahInterval = (semestaU[1] - semestaU[0])/lenInterval
    #* mi nilai tengah
    nilaiTengah = sum(semestaU)/2
    return lenInterval,jumlahInterval,nilaiTengah


def HimpunanFuzzy():
    pass

def FuzzyLogicRelation():
    pass

def FLRGroup():
    pass

def Pembobotan():
    pass

def Defuzzikasi():
    pass

def Mape():
    pass


data = readcsv('Data.csv')
newdata =Prepocessing(data)
monthdata = PlotMonth(newdata[0],newdata[1])
semesta = SemestaU(newdata[1],500,500)
mean = Mean(newdata[1])
interval = IntervalAVG(mean[1],semesta)
# print(type(newdata[0][1]))
count = True

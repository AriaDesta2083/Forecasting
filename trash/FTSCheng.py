import csv
from datetime import datetime
from collections import defaultdict, Counter

#! PEMBUATAN ALGORITMA FUZZY TIME SERIES CHENG


def readcsv(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=";")
        data = []
        tanggal = []
        for row in readCSV:
            tanggal.append(row[1])
            data.append(row[2])
    return tanggal, data


def Prepocessing(data):
    strtanggal = data[0][1:]
    strharga = data[1][1:]
    exharga = [0]
    for i in range(len(strharga)):
        if strharga[i] == "-":
            strharga[i] = 0
    tanggal = [datetime.strptime(x, "%d/%m/%Y") for x in strtanggal]
    harga = list(map(int, strharga))
    minharga = min([x for x in harga if x not in exharga])
    maxharga = max([x for x in harga if x not in exharga])
    newminharga = round(minharga, -2)
    newmaxharga = round(maxharga / 100) * 100
    namahari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    for i in range(len(harga)):
        if harga[i] == 0:
            # *  SELEKSI preposessing data
            if namahari[tanggal[i].weekday()] in ["Sabtu", "Minggu"]:
                harga[i] = 0
                tanggal[i] = 0

            # * NORMALISASI preposessing data
            else:
                pre = (harga[i - 1] - minharga) / (maxharga - minharga) * (
                    newmaxharga - newminharga
                ) + newminharga
                harga[i] = int(round(pre))
    tanggal = [x.date() for x in tanggal if x != 0]
    harga = [x for x in harga if x != 0]
    return tanggal, harga


def PlotMonth(dates, prices):
    # * Membuat kamus defaultdict untuk menyimpan harga-harga per bulan dan tahun
    prices_per_month_year = defaultdict(int)
    count_per_month_year = defaultdict(int)

    # * Mengelompokkan harga-harga per bulan dan tahun dan menghitung jumlah data per bulan dan tahun
    for date, price in zip(dates, prices):
        month_year = date.strftime("%Y-%m")
        prices_per_month_year[month_year] += price
        count_per_month_year[month_year] += 1

    # * Membuat array tanggal baru dan array harga baru
    new_dates = []
    new_prices = []

    # * Mengisi array tanggal baru dan array harga baru dengan nilai rata-rata per bulan dan tahun
    for month_year, price_sum in prices_per_month_year.items():
        count = count_per_month_year[month_year]
        average_price = price_sum / count
        new_dates.append(month_year)
        new_prices.append(int(round(average_price)))

    return new_dates, new_prices


def Filterdata(data, x):
    if x != 0:
        tanggal = [i for i in data[0][x:]]
        harga = [i for i in data[1][x:]]
        return tanggal, harga
    else:
        tanggal = [i for i in data[0]]
        harga = [i for i in data[1]]
        return tanggal, harga


# def round_thousand(data):
#     return data // 1000 * 1000


def SemestaU(data):
    # *masukkan rumus semesta U
    # dmin
    d1 = round(min(data), -2)
    d1 = abs(min(data) - d1)
    # dmax
    d2 = round(max(data) / 100) * 100
    d2 = abs(max(data) - d2)
    U = [min(data) - d1, max(data) + d2]

    return U, d1, d2


def Mean(Data):
    # *masukkan rumus mean
    selisih = []
    for i in range(len(Data)):
        if i == len(Data) - 1:
            break
        val = Data[i + 1] - Data[i]
        selisih.append(abs(val))
    mean = round(sum(selisih) / (len(Data)))
    return selisih, mean


def IntervalAVG(mean, semestaU):
    print(semestaU[1], semestaU[0])
    # * panjang interval
    lenInterval = round(mean / 2)
    # * l jumlah interval
    jumlahInterval = round((semestaU[1] - semestaU[0]) / lenInterval)
    return lenInterval, jumlahInterval


def HimpunanFuzzy(lenInterval, qtyInterval, dmin):
    kelas = []
    bBawah = []
    bAtas = []
    nTengah = []
    nilai = dmin
    dataDict = {}
    for i in range(1, qtyInterval + 1):
        kelas.append("A" + str(i))
        bb = nilai
        ba = nilai + lenInterval
        nt = (bb + ba) / 2
        bBawah.append(int(bb))
        bAtas.append(int(ba))
        nTengah.append(int(nt))
        nilai = ba
    for i in range(1, len(kelas) + 1):
        dataDict[kelas[i - 1]] = {"nilai": nTengah[i - 1]}
    return kelas, bBawah, bAtas, nTengah, dataDict


def FuzzyLogicRelation(kelompok, kelas, data):
    # Menginisialisasi array baru untuk kelompok
    fuzzifikasi = []
    hubflr = []
    # Mengelompokkan nilai dalam data berdasarkan kelompok
    for nilai in data:
        for i, k in enumerate(kelompok):
            if nilai < k:
                fuzzifikasi.append(kelas[i])
                hubflr.append(kelas[i])
                break
    del hubflr[-1]
    hubflr.insert(0, "-")
    return fuzzifikasi, hubflr


def FLRGroup(data):
    # Mengisi kamus berdasarkan data
    dictFLRG = {}
    for i in range(len(data) - 1):
        current_state = data[i]
        next_state = data[i + 1]
        if current_state not in dictFLRG:
            dictFLRG[current_state] = []
        dictFLRG[current_state].append(next_state)
    # Menampilkan hasil
    for current_state, next_states in dictFLRG.items():
        list(set(next_states))
    return dictFLRG


def Pembobotan(data):
    flrg = []
    newflrg = []
    bobot = []
    pembobotan = []
    for i in data:
        element_count = Counter(i)
        # Mengonversi dictionary hasil penghitungan menjadi list
        result = list(element_count.values())
        result2 = list(element_count.keys())
        bobot.append(result)
        flrg.append(result2)
        r = []
        for i in range(len(result)):
            r.append(f"{result2[i]} [{result[i]}]")
        newflrg.append(r)
        comper = [round((x / sum(result)), 3) for x in result]
        pembobotan.append(comper)
    return bobot, pembobotan, flrg, newflrg


def Defuzzikasi(flrgroup, nilaiFuzzy, bobot):
    key = flrgroup.keys()
    value = bobot[2]
    list_key = list(key)
    list_real = []
    list_bobot = list(bobot[1])
    deffuzikasi = []
    list_deffuzikasi = []
    dictDeffuzikasi = {}
    for i in value:
        linguistik = i
        real = [nilaiFuzzy[elem]["nilai"] for elem in linguistik]
        list_real.append(real)
    for i in range(len(list_bobot)):
        x = list_real[i]
        y = list_bobot[i]
        result = [round(x[j] * y[j]) for j in range(len(x))]
        list_deffuzikasi.append(result)
        deffuzikasi.append(int(sum(result)))
    for i in range(len(deffuzikasi)):
        dictDeffuzikasi[list_key[i]] = deffuzikasi[i]
    return dictDeffuzikasi, list_deffuzikasi


def Peramalan(flr, deffuzikasi):
    peramlan = []
    for i in flr:
        peramlan.append(deffuzikasi[i])
    return peramlan


def Mape(dataasli, peramalan):
    di = [i for i in dataasli[1:]]
    fi = [i for i in peramalan[:-1]]
    difilist = []
    didilist = []
    mapelist = []
    for i in range(len(fi)):
        difi = abs(di[i] - fi[i])
        difilist.append(difi)
        didi = difi / di[i]
        didi = round(didi, 3)
        didilist.append(didi)
        mape = didi * 100
        mape = round(mape, 3)
        mapelist.append(mape)
    nilaimape = sum(mapelist) / len(mapelist)
    nilaimape = round(nilaimape, 3)
    return difilist, didilist, mapelist, nilaimape


readdata = readcsv("Data.csv")
dataprepocessing = Prepocessing(readdata)
newdata = Filterdata(dataprepocessing, 0)
if __name__ == "__main__":
    semesta = SemestaU(newdata[1])
    mean = Mean(newdata[1])
    interval = IntervalAVG(mean[1], semesta[0])
    hFuzzy = HimpunanFuzzy(round(interval[0]), round(interval[1]), round(semesta[0][0]))
    fuzzylr = FuzzyLogicRelation(hFuzzy[2], hFuzzy[0], newdata[1])
    flrgroup = FLRGroup(fuzzylr[0])
    bobot = Pembobotan(list(flrgroup.values()))
    deffuzikasi = Defuzzikasi(flrgroup, hFuzzy[4], bobot)
    peramalan = Peramalan(fuzzylr[0], deffuzikasi[0])
    mape = Mape(newdata[1], peramalan)
    print(mape)


#     newdata = Filterdata(dataprepocessing, 0)
#     semesta = SemestaU(newdata[1])
#     mean = Mean(newdata[1])
#     interval = IntervalAVG(mean[1], semesta[0])
#     hFuzzy = HimpunanFuzzy(round(interval[0]), round(interval[1]), round(semesta[0]))
#     fuzzylr = FuzzyLogicRelation(hFuzzy[2], hFuzzy[0], newdata[1])
#     flrgroup = FLRGroup(fuzzylr[0])
#     bobot = Pembobotan(list(flrgroup.values()))
#     deffuzikasi = Defuzzikasi(flrgroup, hFuzzy[4], bobot)
#     peramalan = Peramalan(fuzzylr[0], deffuzikasi[0])
#     mape = Mape(newdata[1], peramalan)
#     print(mape)

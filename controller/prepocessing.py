from datetime import datetime
import math
from controller.readdata import *

#! ENCODING DATA


def prepocessing(data):
    encoddata = encoding_data(data)
    missingvalue = missing_value(encoddata)
    outlier = data_outlier(missingvalue)
    return outlier


def encoding_data(data):
    tanggal, harga = data[0][1:], data[1][1:]
    for i in range(len(harga)):
        if harga[i] == "-":
            harga[i] = math.nan
    new_tanggal = [datetime.strptime(x, "%d/%m/%Y").date() for x in tanggal]
    new_harga = [
        (
            int(nilai)
            if isinstance(nilai, str) and not math.isnan(float(nilai))
            else math.nan
        )
        for nilai in harga
    ]
    # print(f" - tanggal : {type(new_tanggal[0])} | harga : {type(new_harga[0])}")
    return new_tanggal, new_harga


#! MISSING VALUE
def missing_value(data):
    pre_tanggal = mv_tanggal(tanggal=data[0], harga=data[1])
    pre_harga = mv_harga(tanggal=pre_tanggal[0], harga=pre_tanggal[1])
    tanggal, harga = pre_tanggal[0], pre_harga
    return tanggal, harga


def mv_tanggal(tanggal, harga):
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    dictHari = {h: 0 for h in hari}
    count = []
    for t in tanggal:
        dictHari[hari[t.weekday()]] += 1
    for h, c in dictHari.items():
        # print(f"{h} : {c}", end=" | ")
        # print()
        pass
    if dictHari["Sabtu"] == 0 and dictHari["Minggu"] == 0:
        # print(f" - penghapusan missing value : {len(count)}")
        return tanggal, harga
    else:
        for i in range(len(tanggal)):
            if hari[tanggal[i].weekday()] in ["Sabtu", "Minggu"]:
                del tanggal[i]
                del harga[i]
                count.append((tanggal[i], harga[i]))
        # print(f" - penghapusan missing value : {len(count)}")
        return tanggal, harga


def mv_harga(tanggal, harga):
    count = []
    for i in range(len(harga)):
        if math.isnan(harga[i]):
            harga[i] = normalisasi_minmax(
                dbf=harga[i - 1],
                dmin=min(harga),
                dmax=max(harga),
            )
            count.append((tanggal[i], harga[i]))
    # print(f" - pengisian missing value : {len(count)}")
    return harga


def normalisasi_minmax(dbf, dmin, dmax):
    d1 = 500 * math.floor(dmin / 500)
    d2 = 500 * math.ceil(dmax / 500)
    new_dmin = d1 if d1 != dmin else d1 - 500
    new_dmax = d2 if d2 != dmax else d2 + 500
    pre = (dbf - dmin) / (dmax - dmin) * (new_dmax - new_dmin) + new_dmin
    hasil = int(round(pre))
    return hasil


def data_outlier(data):
    tanggal, harga = data
    sorted_harga = sorted(harga)
    q1 = sorted_harga[int(len(harga) * 0.15)]
    q3 = sorted_harga[int(len(harga) * 0.95)]
    iqr = q3 - q1
    min_iqr = q1 - (1.5 * iqr)
    max_iqr = q3 + (1.5 * iqr)
    data_outlier = []
    for i in range(len(harga)):
        if harga[i] < min_iqr or harga[i] > max_iqr:
            data_outlier.append((tanggal[i], harga[i]))
            harga[i] = normalisasi_minmax(
                dbf=harga[i - 1],
                dmin=min_iqr,
                dmax=max_iqr,
            )
    # print(f" - penanganan outlier : {len(data_outlier)}")
    return data


def return_data(data):
    readdata = read_data(data)
    prepocessingdata = prepocessing(readdata)
    return prepocessingdata


if __name__ == "__main__":
    for i in csv_data.keys():
        print(i.upper())
        readdata = read_data(i)
        prepocessingdata = prepocessing(readdata)

from datetime import datetime
import math

#! ENCODING DATA


class Prepocessing:
    def __init__(self, data):
        print("\n| PREPOCESSING |\n")
        print("\n| ENCODING |\n")
        self.encoding = encoding_data(data)
        print("\n| ENCODING SUCCESS |\n")
        print("\n| MISSING VALUE |\n")
        self.missingvalue = missing_value(self.encoding)
        print("\n| MISSING VALUE SUCCESS |\n")
        print("\n| OUTLIER |\n")
        self.outlier = data_outlier(self.missingvalue)
        print("\n| OUTLIER SUCCESS |\n")
        print("\n| PREPOCESSING SUCCESS |\n")


def prepocessing(data):
    print()
    print("| PREPOCESSING |")
    print()
    print("| ENCODING |")
    print()
    encoddata = encoding_data(data)
    print()
    print("| ENCODING SUCCESS |")
    print()
    print("| MISSING VALUE |")
    print()
    missingvalue = missing_value(encoddata)
    print("| MISSING VALUE SUCCESS |")
    print()
    print("| OUTLIER | ")
    print()
    outlier = data_outlier(missingvalue)
    print()
    print("| OUTLIER SUCCESS |")
    print()
    print("| PREPOCESSING SUCCESS |")
    print()
    return outlier


def encoding_data(data):
    tanggal, harga = data[0], data[1]
    print(f"type awal | tanggal : {type(tanggal[1])} | harga : {type(harga[1])} |")
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
    a = list(
        {
            (
                str(type(x))
                if not (isinstance(x, float) and math.isnan(x))
                else "<class 'math.nan'>"
            )
            for x in new_harga
        }
    )
    print(
        f"type akhir | tanggal : {list({str(type(x)) for x in new_tanggal})} | harga : {a} |"
    )
    print()
    return new_tanggal, new_harga


#! MISSING VALUE
def missing_value(data):
    pre_tanggal = mv_tanggal(tanggal=data[0], harga=data[1])
    print()
    pre_harga = mv_harga(tanggal=pre_tanggal[0], harga=pre_tanggal[1])
    print()
    tanggal, harga = pre_tanggal[0], pre_harga
    return tanggal, harga


def mv_tanggal(tanggal, harga):
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    dictHari = {h: 0 for h in hari}
    count = []
    for t in tanggal:
        dictHari[hari[t.weekday()]] += 1
    for h, c in dictHari.items():
        print(f"{h} : {c}", end=" ")
    print()
    if dictHari["Sabtu"] == 0 and dictHari["Minggu"] == 0:
        print(f"mv tanggal : {len(count)}")
        return tanggal, harga
    else:
        new_tanggal = []
        new_harga = []
        for i in range(len(tanggal)):
            if hari[tanggal[i].weekday()] in ["Sabtu", "Minggu"]:
                count.append((tanggal[i], harga[i]))
                print("nm ", tanggal[i], hari[tanggal[i].weekday()])
            else:
                new_tanggal.append(tanggal[i])
                new_harga.append(harga[i])
        print()
        print(f"mv tanggal : {len(count)}")
        return new_tanggal, new_harga


def mv_harga(tanggal, harga):
    count = []
    for i in range(len(harga)):
        if math.isnan(harga[i]):
            print("nm ", tanggal[i], harga[i], end=" >> ")
            harga[i] = normalisasi_minmax(
                dbf=harga[i - 1],
                dmin=min(harga),
                dmax=max(harga),
            )
            count.append((tanggal[i], harga[i]))
    print()
    print(f"mv harga : {len(count)}")
    return harga


def normalisasi_minmax(dbf, dmin, dmax):
    d1, d2 = 500 * math.floor(dmin / 500), 500 * math.ceil(dmax / 500)
    new_dmin, new_dmax = d1 if d1 != dmin else d1 - 500, d2 if d2 != dmax else d2 + 500
    pre = (dbf - dmin) / (dmax - dmin) * (new_dmax - new_dmin) + new_dmin
    hasil = int(round(pre))
    print(hasil)
    return hasil


def data_outlier(data):
    tanggal, harga = data
    sorted_harga = sorted(harga)
    q1 = sorted_harga[int(len(harga) * 0.15)]
    q3 = sorted_harga[int(len(harga) * 0.95)]
    iqr = q3 - q1
    min_iqr = q1 - (1.5 * iqr)
    max_iqr = q3 + (1.5 * iqr)
    count = []
    for i in range(len(harga)):
        if harga[i] < min_iqr or harga[i] > max_iqr:
            count.append((tanggal[i], harga[i]))
            print("nm ", tanggal[i], harga[i], end=" >> ")
            harga[i] = normalisasi_minmax(
                dbf=harga[i - 1],
                dmin=min_iqr,
                dmax=max_iqr,
            )
    print(f"outlier : {len(count)}")
    return data


# def return_data(data):
#     readdata = read_data(data)
#     prepocessingdata = prepocessing(readdata)
#     return prepocessingdata


# if __name__ == "__main__":
#     for i in csv_data.keys():
#         print(i.upper())
#         readdata = read_data(i)
#         prepocessingdata = prepocessing(readdata)

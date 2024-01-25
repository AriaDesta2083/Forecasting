from datetime import timedelta
from math import nan
import pandas as pd
from FTSChengupdate import *

newdata = Filterdata(dataprepocessing, 0)

start_date = newdata[0][0]
tanggal_hari_ini = datetime.now()
tanggal_besok = tanggal_hari_ini + timedelta(days=1)
end_date = tanggal_besok.strftime("%Y-%m-%d")
hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
date_range = pd.date_range(start=start_date, end=end_date, freq="D")
formatted_dates = date_range.strftime("%Y-%m-%d")
tanggal_peramalan = []

for i in range(len(formatted_dates)):
    if hari[date_range[i].weekday()] in ["Sabtu", "Minggu"]:
        # print(formatted_dates[i], hari[date_range[i].weekday()])
        pass
    else:
        # print(formatted_dates[i], hari[date_range[i].weekday()])
        tanggal_peramalan.append(date_range[i].strftime("%Y-%m-%d"))

newdata = Filterdata(dataprepocessing, 0)
jumlah_peramalan = abs(len(newdata[0]) - len(tanggal_peramalan))

# jumlah_peramalan = 500

# print(jumlah_peramalan)

# * FILTER DATA
newdata = Filterdata(dataprepocessing, 0)
tanggal = newdata[0]
harga = newdata[1]

# * SEMESTA U
semesta = SemestaU(newdata[1])
u = semesta[0]
d1 = semesta[1]
d2 = semesta[2]

# * MEAN
mean = Mean(harga)

# * INTERVAL
interval = Interval(mean, u)
panjang_interval = interval[0]
jumlah_interval = interval[1]


# * HIMPUNAN FUZZY
himpunan_fuzzy = HimpunanFuzzy(panjang_interval, jumlah_interval, u)
list_kelas = himpunan_fuzzy[0]
list_bawah = himpunan_fuzzy[1]
list_atas = himpunan_fuzzy[2]
list_tengah = himpunan_fuzzy[3]
dict_nilai_tengah = himpunan_fuzzy[4]


# * FUZZIFIKASI
fuzzifikasi = Fuzzifikasi(list_atas, list_kelas, harga)

# * FUZZY LOGIC RELATIONSHIP
flr = FuzzyLogicRelationship(fuzzifikasi)

# * FUZZY LOGIC RELATIONSHIP GROUP
flrg = FuzzyLogictRelationshipGroup(fuzzifikasi)
grup = list(flrg.keys())
relasi = list(flrg.values())


# * PEMBOBOTAN
pembobotan = Pembobotan(relasi)
newflrg = pembobotan[0]
bobot = pembobotan[1]
map_bobot = pembobotan[2]


# * DEFUZZIFIKASI
defuzzikasi = Defuzzikasi(grup, map_bobot, dict_nilai_tengah)
dict_deffuzikasi = defuzzikasi[0]
list_deffuzikasi = defuzzikasi[1]

# * PERAMALAN
peramalan = Peramalan(fuzzifikasi, dict_deffuzikasi, dict_nilai_tengah)

# * MAPE
mape = Mape(harga, peramalan)
nilai_mape = mape[0]
list_difi = mape[1]
list_didi = mape[2]
list_mape = mape[3]


def prediksi(harga, peramalan, jumlah_peramalan):
    databaru = [i for i in harga]
    for i in range(0, jumlah_peramalan):
        databaru.append(peramalan[-1])
        # print(peramalan[-1])
        # * SEMESTA U
        semesta = SemestaU(databaru)
        u = semesta[0]
        d1 = semesta[1]
        d2 = semesta[2]
        # * MEAN
        mean = Mean(databaru)
        # * INTERVAL
        interval = Interval(mean, u)
        panjang_interval = interval[0]
        jumlah_interval = interval[1]
        # * HIMPUNAN FUZZY
        himpunan_fuzzy = HimpunanFuzzy(panjang_interval, jumlah_interval, u)
        list_kelas = himpunan_fuzzy[0]
        list_bawah = himpunan_fuzzy[1]
        list_atas = himpunan_fuzzy[2]
        list_tengah = himpunan_fuzzy[3]
        dict_nilai_tengah = himpunan_fuzzy[4]
        # * FUZZIFIKASI
        fuzzifikasi = Fuzzifikasi(list_atas, list_kelas, databaru)
        # * FUZZY LOGIC RELATIONSHIP
        flr = FuzzyLogicRelationship(fuzzifikasi)
        # * FUZZY LOGIC RELATIONSHIP GROUP
        flrg = FuzzyLogictRelationshipGroup(fuzzifikasi)
        grup = list(flrg.keys())
        relasi = list(flrg.values())
        # * PEMBOBOTAN
        pembobotan = Pembobotan(relasi)
        newflrg = pembobotan[0]
        bobot = pembobotan[1]
        map_bobot = pembobotan[2]
        # * DEFUZZIFIKASI
        defuzzikasi = Defuzzikasi(grup, map_bobot, dict_nilai_tengah)
        dict_deffuzikasi = defuzzikasi[0]
        list_deffuzikasi = defuzzikasi[1]
        # * PERAMALAN
        peramalan = Peramalan(fuzzifikasi, dict_deffuzikasi, dict_nilai_tengah)
        # * MAPE
        mape = Mape(databaru, peramalan)
        nilai_mape = mape[0]
        list_difi = mape[1]
        list_didi = mape[2]
        list_mape = mape[3]
    return databaru, mape, nilai_mape


dataprediksi = prediksi(harga, peramalan, jumlah_peramalan)
print(dataprediksi[2])


new_tanggal = tanggal_peramalan
new_harga = harga + [nan for i in range(0, jumlah_peramalan)]
new_peramalan = peramalan + dataprediksi[0][len(harga) :]

print(new_tanggal)
# for i in range(len(new_tanggal)):
#     print(new_tanggal[i], new_harga[i], new_peramalan[i])

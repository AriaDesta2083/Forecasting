# from controller.readdata import add
# from datetime import date, datetime, timedelta
# from math import nan
# import pandas as pd
# from controller.forecasting import Forecasting
# from controller.prepocessing import return_data

# #! import data

from datetime import timedelta
from math import nan


def besok(tanggal):
    besok = (
        tanggal + timedelta(days=3)
        if tanggal.weekday() == 4
        else (
            tanggal + timedelta(days=2)
            if tanggal.weekday() == 5
            else tanggal + timedelta(days=1)
        )
    )
    return besok


def build_forecast(data):
    tanggal = data.tanggal + [besok(data.tanggal[-1])]
    harga = data.harga + [nan]
    peramalan = [nan] + data.peramalan
    return tanggal, harga, peramalan


# def build_forecast(read_data, enddate, dataupdate):
#     # def build_forecast(read_data):
#     if dataupdate:
#         enddate = enddate - timedelta(days=1)
#     z = Forecasting(read_data)
#     start_date = z.tanggal[0]
#     tanggal_hari_ini = date(2024, 4, 4)
#     # testanggal = date(2024, 1, 11) + timedelta(days=30)
#     # tanggal_hari_ini = testanggal
#     tanggal_besok = (
#         tanggal_hari_ini + timedelta(days=3)
#         if tanggal_hari_ini.weekday() == 4
#         else (
#             tanggal_hari_ini + timedelta(days=2)
#             if tanggal_hari_ini.weekday() == 5
#             else tanggal_hari_ini + timedelta(days=1)
#         )
#     )

#     end_date = tanggal_besok.strftime("%Y-%m-%d")
#     hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
#     date_range = pd.date_range(start=start_date, end=end_date, freq="D")
#     formatted_dates = date_range.strftime("%Y-%m-%d")

#     tanggal_peramalan = [
#         date_range[i].strftime("%Y-%m-%d")
#         for i in range(len(formatted_dates))
#         if hari[date_range[i].weekday()] not in ["Sabtu", "Minggu"]
#     ]

#     jumlah_peramalan = len(tanggal_peramalan) - len(z.tanggal)
#     return tanggal_peramalan, jumlah_peramalan, z


# def rounded_value(x):
#     remainder = x % 100
#     if remainder < 50:
#         return x - remainder
#     elif remainder < 75:
#         return x - remainder + 50
#     else:
#         return x - remainder + 100


# def prediksi(harga, tanggal, jumlah_peramalan):
#     hargaperamalan = [i for i in harga]
#     for i in range(0, jumlah_peramalan):
#         za = Forecasting((tanggal, hargaperamalan))
#         if i < jumlah_peramalan:
#             hargaperamalan.append(za.peramalan[-1])
#     za.harga = harga + [nan for i in range(jumlah_peramalan)]
#     za.peramalan = [nan] + za.peramalan
#     return za


# tanggal_peramalan, jumlah_peramalan, z = build_forecast(return_data("Papua"))
# az = prediksi(z.harga, tanggal_peramalan, jumlah_peramalan)


# if __name__ == "__main__":
#     az.flr = az.flr + [f"{z.fuzzifikasi[-1]} →"]
#     print(len(az.tanggal), len(az.harga), len(az.peramalan), len(az.flr))
#     a = []
#     for i in range(len(az.tanggal)):
#         a.append(
#             [
#                 az.tanggal[i],
#                 az.harga[i],
#                 az.flr[i],
#                 az.peramalan[i],
#             ]
#         )
#     print(a)

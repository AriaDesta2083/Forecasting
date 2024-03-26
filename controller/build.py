from datetime import datetime, timedelta
from math import nan
import pandas as pd
from controller.forecasting import Forecasting
from controller.prepocessing import return_data

#! import data


def build_forecast(read_data):
    z = Forecasting(read_data)

    start_date = z.tanggal[0]
    tanggal_hari_ini = datetime.now()
    tanggal_besok = (
        tanggal_hari_ini + timedelta(days=3)
        if tanggal_hari_ini.weekday() == 4
        else (
            tanggal_hari_ini + timedelta(days=2)
            if tanggal_hari_ini.weekday() == 5
            else tanggal_hari_ini + timedelta(days=1)
        )
    )

    end_date = tanggal_besok.strftime("%Y-%m-%d")
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    formatted_dates = date_range.strftime("%Y-%m-%d")

    tanggal_peramalan = [
        date_range[i].strftime("%Y-%m-%d")
        for i in range(len(formatted_dates))
        if hari[date_range[i].weekday()] not in ["Sabtu", "Minggu"]
    ]

    jumlah_peramalan = len(tanggal_peramalan) - len(z.tanggal)
    return tanggal_peramalan, jumlah_peramalan, z


def prediksi(harga, tanggal, jumlah_peramalan):
    hargaperamalan = [i for i in harga]
    for i in range(0, jumlah_peramalan):
        za = Forecasting((tanggal, hargaperamalan))
        if i != jumlah_peramalan - 1:
            hargaperamalan.append(za.peramalan[-1])
    za.harga = harga + [nan for i in range(jumlah_peramalan)]
    za.peramalan = [nan] + za.peramalan
    return za


tanggal_peramalan, jumlah_peramalan, z = build_forecast(return_data("Papua"))
az = prediksi(z.harga, tanggal_peramalan, jumlah_peramalan)


if __name__ == "__main__":
    az.flr = az.flr + [f"{z.fuzzifikasi[-1]} →"]
    print(len(az.tanggal), len(az.harga), len(az.peramalan), len(az.flr))
    a = []
    for i in range(len(az.tanggal)):
        a.append(
            [
                az.tanggal[i],
                az.harga[i],
                az.flr[i],
                az.peramalan[i],
            ]
        )
    print(a)

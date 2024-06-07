from datetime import date, timedelta
from controller.api import *
from controller.forecasting import *
from controller.prepocessing import *


if __name__ == "__main__":
    print(date.today())
    print(date.today() - timedelta(days=360 * 3))
    print()
    print(datetime.now())
    print(datetime.now() - timedelta(days=360 * 3))

    # end_date = date(2024, 4, 4)
    # start_date = end_date - timedelta(days=360 * 3)
    # prov_dict = get_list_wilayah()
    # list_prov = ["Indonesia"] + list(prov_dict.keys())
    # list_mape = []
    # id_prov = prov_dict.get("Indonesia")
    # data, tanggal, harga = get_api(id_prov if id_prov else "", end_date, start_date)
    # for i in range(len(tanggal)):
    #     print(tanggal[i])
    # for i in range(len(tanggal)):
    #     print(harga[i])
    # for i in list_prov:
    #     id_prov = prov_dict.get(i)
    #     data, tanggal, harga = get_api(id_prov if id_prov else "", end_date, start_date)
    #     z = Forecasting(prepocessing((tanggal, harga)))
    #     print()
    #     print("====================================================")
    #     print(f"Gula Pasir Lokal {i}")
    #     print(z.nilai_mape)
    #     list_mape.append(z.nilai_mape)
    #     print("====================================================")
    #     print()
    # print()
    # print("====================================================")
    # print()
    # for i in range(len(list_prov)):
    #     print(list_prov[i], list_mape[i])
    #     print()
    # print("====================================================")
    # print()


# Gula Pasir Lokal Indonesia
# Gula Pasir Lokal Aceh
# Gula Pasir Lokal Bali
# Gula Pasir Lokal Banten
# Gula Pasir Lokal Bengkulu
# Gula Pasir Lokal DI Yogyakarta
# Gula Pasir Lokal DKI Jakarta
# Gula Pasir Lokal Gorontalo
# Gula Pasir Lokal Jambi
# Gula Pasir Lokal Jawa Barat
# Gula Pasir Lokal Jawa Tengah
# Gula Pasir Lokal Jawa Timur
# Gula Pasir Lokal Kalimantan Barat
# Gula Pasir Lokal Kalimantan Selatan
# Gula Pasir Lokal Kalimantan Tengah
# Gula Pasir Lokal Kalimantan Timur
# Gula Pasir Lokal Kalimantan Utara
# Gula Pasir Lokal Kepulauan Bangka Belitung
# Gula Pasir Lokal Kepulauan Riau
# Gula Pasir Lokal Lampung
# Gula Pasir Lokal Maluku
# Gula Pasir Lokal Maluku Utara
# Gula Pasir Lokal Nusa Tenggara Barat
# Gula Pasir Lokal Nusa Tenggara Timur
# Gula Pasir Lokal Papua
# Gula Pasir Lokal Papua Barat
# Gula Pasir Lokal Riau
# Gula Pasir Lokal Sulawesi Barat
# Gula Pasir Lokal Sulawesi Selatan
# Gula Pasir Lokal Sulawesi Tengah
# Gula Pasir Lokal Sulawesi Tenggara
# Gula Pasir Lokal Sulawesi Utara
# Gula Pasir Lokal Sumatera Barat
# Gula Pasir Lokal Sumatera Selatan
# Gula Pasir Lokal Sumatera Utara

# 0.35
# 0.21
# 0.19
# 0.13
# 0.22
# 0.2
# 0.2
# 0.31
# 0.27
# 0.12
# 0.24
# 0.2
# 0.32
# 0.2
# 0.17
# 0.38
# 0.25
# 0.16
# 0.29
# 0.15
# 0.19
# 0.27
# 0.17
# 0.1
# 0.37
# 0.2
# 0.16
# 0.18
# 0.23
# 0.17
# 0.23
# 0.19
# 0.21
# 0.34
# 0.21

from controller.readdata import *
from controller.prepocessing import return_data
from controller.FTSChengupdate import *


class Forecasting:
    def __init__(self, data):
        self.data = data
        self.tanggal, self.harga = data
        self.u = SemestaU(self.harga)
        self.mean = Mean(self.harga)
        self.panjang_interval, self.jumlah_interval = Interval(self.mean, self.u)
        (
            self.list_kelas,
            self.list_bawah,
            self.list_atas,
            self.list_tengah,
            self.nilai_tengah,
        ) = HimpunanFuzzy(self.panjang_interval, self.jumlah_interval, self.u)
        self.fuzzifikasi = Fuzzifikasi(self.list_atas, self.list_kelas, self.harga)
        self.flr = FuzzyLogicRelationship(self.fuzzifikasi)
        self.flrg = FuzzyLogicRelationshipGroup(self.fuzzifikasi)
        self.grup = list(self.flrg.keys())
        self.relasi = list(self.flrg.values())
        self.pembobotan = Pembobotan(self.relasi)
        self.newflrg, self.bobot, self.map_bobot = self.pembobotan
        self.defuzzifikasi = Defuzzifikasi(self.grup, self.map_bobot, self.nilai_tengah)
        self.dict_defuzzifikasi, self.list_defuzzifikasi = self.defuzzifikasi
        self.peramalan = Peramalan(
            self.fuzzifikasi, self.dict_defuzzifikasi, self.nilai_tengah
        )
        self.nilai_mape, self.list_difi, self.list_didi, self.list_mape = Mape(
            self.harga, self.peramalan
        )


if __name__ == "__main__":
    # for i in csv_data.keys():
    forecast = Forecasting(return_data("Jawa Timur"))
    # print(forecast.nilai_mape)
    # print(forecast.mean)
    # # print(forecast.panjang_interval)
    # for i in range(len(forecast.defuzzifikasi)):
    for i in range(len(forecast.grup)):
        if i < 3 or i > len(forecast.grup) - 4:
            print(f"{[i]}")
        #     # print(forecast.defuzzifikasi[i])
        #     print(forecast.defuzzifikasi[i])
        else:
            pass

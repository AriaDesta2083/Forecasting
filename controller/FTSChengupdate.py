from collections import Counter
import math
import os
from controller.prepocessing import *

#! PEMBUATAN ALGORITMA FUZZY TIME SERIES CHENG


def SemestaU(data):
    d1, d2 = 500 * math.floor(min(data) / 500), 500 * math.ceil(max(data) / 500)
    U = [d1 if d1 != min(data) else d1 - 500, d2 if d2 != max(data) else d2 + 500]
    return U


def Mean(harga):
    selisih = [abs(harga[i + 1] - harga[i]) for i in range(len(harga) - 1)]
    return round(sum(selisih) / len(harga), 5)


def Interval(mean, u):
    panjang_interval = round(mean / 2, 5)
    jumlah_interval = round((u[1] - u[0]) / panjang_interval)
    return panjang_interval, jumlah_interval


def HimpunanFuzzy(panjang_interval, jumlah_interval, u):
    dict_nilai_tengah = {}
    list_kelas = [f"A{i}" for i in range(1, jumlah_interval + 1)]
    list_bawah = [
        round(u[0] + (i - 1) * panjang_interval, 5)
        for i in range(1, jumlah_interval + 1)
    ]
    list_atas = [round(bawah + panjang_interval, 5) for bawah in list_bawah]
    list_tengah = [(bawah + atas) // 2 for bawah, atas in zip(list_bawah, list_atas)]
    for i in range(1, len(list_kelas) + 1):
        dict_nilai_tengah[list_kelas[i - 1]] = list_tengah[i - 1]
    return list_kelas, list_bawah, list_atas, list_tengah, dict_nilai_tengah


def Fuzzifikasi(list_atas, list_kelas, harga):
    fuzzifikasi = []
    for nilai in harga:
        for i, k in enumerate(list_atas):
            if nilai < k:
                fuzzifikasi.append(list_kelas[i])
                break
    return fuzzifikasi


def FuzzyLogicRelationship(fuzzifikasi):
    flr = [
        f" → {fuzzifikasi[i]}" if i == 0 else f"{fuzzifikasi[i-1]} → {fuzzifikasi[i]}"
        for i in range(len(fuzzifikasi))
    ]
    return flr


def FuzzyLogicRelationshipGroup(fuzzifikasi):
    dictFLRG = {}
    for i in range(len(fuzzifikasi) - 1):
        grup = fuzzifikasi[i]
        relasi = fuzzifikasi[i + 1]
        if grup not in dictFLRG:
            dictFLRG[grup] = []
        dictFLRG[grup].append(relasi)
    return dictFLRG


def Pembobotan(relasi):
    newflrg = []
    bobot = []
    map_bobot = []
    for i in relasi:
        element_count = Counter(i)
        linguistik = list(element_count.keys())
        kemunculan = list(element_count.values())
        x, y, z = (
            [f"{linguistik[i]}  ({kemunculan[i]})" for i in range(len(linguistik))],
            [round((x / sum(kemunculan)), 5) for x in kemunculan],
            [
                [linguistik[i], round((kemunculan[i] / sum(kemunculan)), 5)]
                for i in range(len(linguistik))
            ],
        )
        newflrg.append(x), bobot.append(y), map_bobot.append(z)
    return newflrg, bobot, map_bobot


def Defuzzifikasi(grup, map_bobot, dict_nilai_tengah):
    dict_defuzzifikasi = {}
    list_defuzzifikasi = []
    for i in range(len(map_bobot)):
        defuzz = [round(dict_nilai_tengah[i[0]] * i[1], 5) for i in map_bobot[i]]
        list_defuzzifikasi.append(defuzz)
        dict_defuzzifikasi[grup[i]] = round(sum(defuzz))
    return dict_defuzzifikasi, list_defuzzifikasi


def Peramalan(fuzzifikasi, dict_defuzzifikasi, dict_nilai_tengah):
    peramalan = [
        dict_defuzzifikasi[i] if i in dict_defuzzifikasi else dict_nilai_tengah[i]
        for i in fuzzifikasi
    ]
    return peramalan


def Mape(harga, peramalan):
    list_difi = [abs(harga[i + 1] - peramalan[i]) for i in range(len(peramalan) - 1)]
    list_didi = [round(list_difi[i] / harga[i + 1], 5) for i in range(len(list_difi))]
    list_mape = [round(list_didi[i] * 100, 2) for i in range(len(list_didi))]
    nilai_mape = round(sum(list_mape) / len(list_mape), 2)
    return nilai_mape, list_difi, list_didi, list_mape


def tampilkan_menu():
    # clear_console()
    print("=== Menu ===")
    print("1. Data Aktual")
    print("2. Semesta U")
    print("3. Interval")
    print("4. Himpunan Fuzzy")
    print("5. Fuzzifikasi")
    print("6. FLR")
    print("7. FLRG")
    print("8. Pembobotan")
    print("9. Defuzifikasi")
    print("10. Peramalan")
    print("11. Mape")
    print("0. Keluar")
    print()


def clear_console():
    # Clear console screen
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    # * FILTER DATA
    # for i in range(len(list(csv_data.keys()))):
    #     print(f"{i+1}. {list(csv_data.keys())[i]}")
    # wilayah = int(input("Masukkan nama wilayah: "))
    data = return_data("Aceh")
    newdata = prepocessing(data)
    tanggal, harga = newdata[0], newdata[1]
    # * SEMESTA U
    u = SemestaU(harga)
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
    flrg = FuzzyLogicRelationshipGroup(fuzzifikasi)
    grup = list(flrg.keys())
    relasi = list(flrg.values())
    # * PEMBOBOTAN
    pembobotan = Pembobotan(relasi)
    newflrg = pembobotan[0]
    bobot = pembobotan[1]
    map_bobot = pembobotan[2]
    # * DEFUZZIFIKASI
    defuzzifikasi = Defuzzifikasi(grup, map_bobot, dict_nilai_tengah)
    dict_defuzzifikasi = defuzzifikasi[0]
    list_defuzzifikasi = defuzzifikasi[1]
    # * PERAMALAN
    peramalan = Peramalan(fuzzifikasi, dict_defuzzifikasi, dict_nilai_tengah)
    # * MAPE
    mape = Mape(harga, peramalan)
    nilai_mape = mape[0]
    list_difi = mape[1]
    list_didi = mape[2]
    list_mape = mape[3]

    def main(
        tanggal,
        harga,
        u,
        panjang_interval,
        jumlah_interval,
        list_kelas,
        list_bawah,
        list_atas,
        list_tengah,
        fuzzifikasi,
        flr,
        grup,
        relasi,
        newflrg,
        bobot,
        map_bobot,
        dict_defuzzifikasi,
        list_defuzzifikasi,
        peramalan,
        nilai_mape,
        list_difi,
        list_didi,
        list_mape,
    ):
        x = [" \t "]
        y = [f"{fuzzifikasi[-1]} → "]
        a = [str(i) for i in tanggal] + x
        b = [str(i) for i in harga] + x
        c = [str(i) for i in flr] + y
        d = x + [str(i) for i in peramalan]
        e = x + [i for i in list_difi] + x
        f = x + [i for i in list_didi] + x
        g = x + [i for i in list_mape] + [f"{nilai_mape}"]
        while True:
            tampilkan_menu()
            pilihan = input("Masukkan nomor pilihan: ")
            if pilihan == "1":
                # Implementasi untuk Pilihan 1
                clear_console()
                print(" |\tData Aktual\t|")
                print()
                print("| TANGGAL | HARGA |")
                print()
                for i in range(len(tanggal)):
                    print(f" | {harga[i-1]} |\t{tanggal[i]} | {harga[i-2]} |")
                print()
                input("Tekan Enter untuk kembali ke menu...")
            elif pilihan == "2":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Semesta U | ")
                print(f"dmin\t : {min(harga)}")
                print(f"dmax\t : {max(harga)}")
                print(f"d1\t : {min(harga)-u[0]}")
                print(f"d2\t : {u[1]-max(harga)}")
                print()
                print(f"semesata u\t : {u}")
                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "3":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Interval | ")
                print(f"mean : {mean}")
                print(f"panjang interval : {panjang_interval}")
                print(f"jumlah interval : {jumlah_interval}")
                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "4":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Himpunan Fuzzy | ")
                print(f" Kelas | Batas Atas | Batas Bawah | Nilai Tengah")

                for i in range(len(list_kelas)):
                    print(
                        f" {list_kelas[i]}\t| {round(list_atas[i])} | {round(list_bawah[i])} | {round(list_tengah[i])}"
                    )
                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "5":
                # Implementasi untuk Pilihan 2
                clear_console()

                print(" |  Fuzzifikasi | ")
                print()
                for i in range(0, len(harga), 3):
                    print(f"|{tanggal[i]}|{harga[i]}|{fuzzifikasi[i]}|")
                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "6":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  FLR | ")
                print()
                for i in range(len(harga)):
                    print(i)
                    print(f"|{tanggal[i]}|{harga[i]}|{flr[i]}|")
                print()

                input("Tekan Enter untuk kembali ke menu...")
            elif pilihan == "7":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  FLRG | ")
                print()
                for i in range(len(grup)):
                    print(i + 1)
                    print(f"{grup[i]}|{relasi[i]}")
                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "8":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Pembobotan | ")
                print()
                for i in range(len(bobot)):
                    if i < 6 or i > len(bobot) - 6:
                        print(f"{grup[i]}|{newflrg[i]}|{bobot[i]}")
                    else:
                        pass
                print()

                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "9":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Defuzifikasi | ")
                print()
                for i in range(len(grup)):
                    if i < 6 or i > len(grup) - 6:
                        print(f"{grup[i]}")
                        for z in map_bobot[i]:
                            print(f"{z[0]}({z[1]})", end=" , ")
                        print()
                        print(f"{list_defuzzifikasi[i]}")
                    else:
                        pass
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "10":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Peramalan | ")
                for i in range(len(a)):
                    if i < 6 or i > len(a) - 6:
                        print(f"xx {a[i]}\n yy {b[i]}\n zz {c[i]}\n uu {d[i]}\n")
                    else:
                        pass
                print("hasil peramalan  ")
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "11":
                # Implementasi untuk Pilihan 2
                clear_console()
                print(" |  Mape | ")
                print()
                for i in range(len(e)):
                    print(f"| {a[i]} | {b[i]} | {d[i]} | {e[i]} | {f[i]}\t| {g[i]} |")
                print()
                input("Tekan Enter untuk kembali ke menu...")

            elif pilihan == "0":
                clear_console()
                print("Keluar dari program. Sampai jumpa!")
                break
            else:
                clear_console()
                print("Pilihan tidak valid. Silakan coba lagi.")

    main(
        tanggal,
        harga,
        u,
        panjang_interval,
        jumlah_interval,
        list_kelas,
        list_bawah,
        list_atas,
        list_tengah,
        fuzzifikasi,
        flr,
        grup,
        relasi,
        newflrg,
        bobot,
        map_bobot,
        dict_defuzzifikasi,
        list_defuzzifikasi,
        peramalan,
        nilai_mape,
        list_difi,
        list_didi,
        list_mape,
    )

#! FIX
#! fitur
# readcsv -> done
# Prepocessing -> done
# Filterdata -> done
# SemestaU -> done
# Mean -> done
# Interval -> done
# HimpunanFuzzy -> done
# Fuzzifikasi -> done
# FuzzyLogicRelationship -> done
# FuzzyLogicRelationshipGroup -> done
# Pembobotan -> done
# Defuzzifikasi -> done
# Peramalan -> done
# Mape -> done
# tampilkan_menu -> done
# clear_console -> done
# main -> done

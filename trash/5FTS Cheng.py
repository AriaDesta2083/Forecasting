import streamlit as st
from trash.FTSCheng import *
from annotated_text import annotated_text, annotation
import pandas as pd

# Judul aplikasi
st.set_page_config(page_title="FTS Cheng", page_icon="images/unej.png")
st.header("Implementasi Fuzzy Time Series Cheng")
# annotated_text(
#     "Pada tahap ",
#     ("implementasi", ""),
#     " sejumlah kegiatan penting akan dilakukan untuk ",
#     ("mengolah data", ""),
#     "yang telah disiapkan. Sistem ini akan melakukan serangkaian langkah, seperti menghitung ",
#     ("himpunan semesta", "universe of discourse"),
#     ", menentukan ",
#     ("interval", "fuzzy"),
#     " menghitung",
#     ("himpunan", "fuzzy"),
#     " proses ",
#     ("fuzzifikasi", ""),
#     " mengembangkan relasi logika fuzzy,",
#     ("Fuzzy Logic Relatationship", "FLR"),
#     " membentuk kelompok relasi logika fuzzy",
#     ("Fuzzy Logic Relatationship Group", "FLRG"),
#     " menghitung matriks ",
#     ("pembobotan", ""),
#     " terstandarisasi, melakukan ",
#     ("defuzzifikasi", ""),
#     " melakukan",
#     ("peramalan", ""),
#     " melakukan ",
#     ("pengujian", ""),
#     " dan menghasilkan nilai ",
#     ("Mean Absolute Percentage Error", "MAPE"),
#     " sebagai indikator tingkat kesalahan peramalan harga gula. Hasil dari sistem ini akan mencakup proses perhitungan peramalan dan nilai MAPE yang menggambarkan akurasi peramalan harga gula.Bahasa pemrograman yang digunakan untuk mengimplementasikan sistem ini adalah ",
#     ("Python", ""),
# )

day = st.slider("Pilih jangka data peramalan", 1, len(dataprepocessing[0]) - 99, 1)
st.write("Start data ", dataprepocessing[0][day - 1], " - ", dataprepocessing[0][-1])
newdata = Filterdata(dataprepocessing, day - 1)
st.write("Panjang Data :", len(newdata[0]))
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
st.write("MAPE :", mape[3], "%")


# *PROSES CHENG


# * Tautan ke halaman Himpunan Semesta

if st.sidebar.button("Himpunan Semesta U"):
    b1, b2, b3 = st.columns([0.1, 0.1, 0.3])
    hs = f"""
        Dmin = {min(newdata[1])}
        Dmax = {max(newdata[1])}
        D1 = {semesta[1]}
        D2 = {semesta[2]}
    """
    annotated_text(
        annotation(
            "HIMPUNAN SEMESTA ",
            "U ",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahapan pembentukan",
        ("himpunan semesta", "U"),
        " membutuhkan nilai ",
        ("Data Tertinggi", "Dmax"),
        " nilai",
        ("Data Terendah", "Dmin"),
        "dan nilai",
        ("Bilangan Konstanta yang ditentukan oleh peneliti.", "D1 dan D2"),
    )
    st.code(hs, language="python")
    b1, b2 = st.columns([0.1, 0.5])
    b1.code("Rumus", language="Python")
    b2.latex(
        r"""
        U= [Dmin-D1 ; Dmax  +D2 ]
        """
    )
    b1.code("Hasil", language="Python")
    b2.latex(
        f"""
        U= [ {semesta[0][0]}  ; {semesta[0][1]} ]
    """
    )

# * Tautan ke halaman Interval Fuzzy

if st.sidebar.button("Interval Fuzzy"):
    #! MEAN
    annotated_text(
        annotation(
            "Menentukan panjang interval",
            "berbasis rata-rata",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        " Tahapan ini mencari nilai ",
        ("Mean", ""),
        " nilai ",
        (" panjang interval", "l"),
        " nilai",
        ("jumlah interval", "p"),
        " dan setelah itu mencari ",
        ("nilai tengah untuk seluruh jumlah interval", "Mi"),
    )

    annotated_text(
        ("A", "."),
        " Menghitung selisih nilai",
        ("𝐷𝑡+1 dan 𝐷1", ""),
        " pada data hingga diperoleh ",
        ("rata-rata selisih", ""),
        " dengan mengikuti persamaan berikut.",
    )
    b1, b2 = st.columns([0.1, 0.5])
    b1.code("Rumus")
    b2.latex(
        r"""
        \text{Mean} = \frac{\sum_{t=1}^n (D_{t+1} - D_1)}{n}
        """
    )
    b1.code("Hasil")
    b2.latex(
        f"""
        Mean = {round(mean[1])}
        """
    )
    st.code(
        """
    #Keterangan
    Mean = Nilai Rata-Rata 
    n = Jumlah Data
    𝐷(𝑡) = Data pada waktu ke (t)
    """,
        language="python",
    )
    #! PANJANG INTERVAL
    annotated_text(
        ("B", "."),
        " Menghitung ",
        (" panjang interval", "l"),
        " dengan mengikuti persamaan berikut",
    )
    b1, b2 = st.columns([0.1, 0.5])
    b1.code("Rumus")
    b2.latex(
        r"""
        l = \frac{\text{Mean}}{2}
        """
    )
    b1.code("Hasil")
    b2.latex(
        f"""
        l = {round(interval[0])}
        """
    )
    st.code(
        """
    #Keterangan
    𝑙 : Panjang interval
    """,
        language="python",
    )
    #! JUMLAH INTERVAL
    annotated_text(
        ("C", "."),
        " Menghitung ",
        ("jumlah interval", "p"),
        " dengan mengikuti persamaan berikut",
    )
    b1, b2 = st.columns([0.1, 0.5])
    b1.code("Rumus")
    b2.latex(
        r"""
    p = \frac{(D_{\text{max}} + D_2) - (D_{\text{min}} - D_1)}{l}
        """
    )
    b1.code("Hasil")
    b2.latex(
        f"""
        p = {round(interval[1])}
        """
    )
    st.code(
        """
    #Keterangan
    p = jumlah interval
    """,
        language="python",
    )

# * Tautan ke halaman Himpunan Fuzzy
if st.sidebar.button("Himpunan Fuzzy"):
    annotated_text(
        annotation(
            "Himpunan Fuzzy",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    l = str(round(interval[0]))
    p = str(round(interval[1]))

    annotated_text(
        ("himpunan fuzzy", ""),
        " dibentuk dengan membagi rentang nilai variabel sepanjang ",
        (" panjang interval", l),
        "sebanyak",
        (" jumlah interval", p),
    )
    himpunanFuzzy = {
        "Kelas": hFuzzy[0],
        "Batas Bawah": hFuzzy[1],
        "Batas Atas": hFuzzy[2],
        "Nilai Tengah": hFuzzy[3],
    }
    df = pd.DataFrame(himpunanFuzzy).set_index("Kelas")
    st.dataframe(df, width=800, height=500)

# * Tautan ke halaman Fuzzifikasi
if st.sidebar.button("Fuzzifikasi"):
    annotated_text(
        annotation(
            "Fuzzifikasi",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahapan ",
        ("fuzzifikasi", ""),
        " dilakukan dengan cara mengubah data",
        (" variabel non-fuzzy", "numerik"),
        "menjadi",
        ("variabel fuzzy", "linguistik"),
        " dari setiap interval yang telah diperoleh. ",
    )
    flr = {
        "Tanggal": newdata[0],
        "Harga": newdata[1],
        "Fuzzifikasi": fuzzylr[0],
    }

    df = pd.DataFrame(flr).set_index("Tanggal")
    st.dataframe(df, width=800, height=400)

# * Tautan ke halaman FLR
if st.sidebar.button("FLR"):
    flr = []
    for i in range(len(fuzzylr[0])):
        flr.append(f"{fuzzylr[1][i]} → {fuzzylr[0][i]}")
    annotated_text(
        annotation(
            "Fuzzy Logic Relationship",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahap pembentukan",
        ("Fuzzy Logic Relatationship", "FLR"),
        " dilakukan berdasarkan data historis yang sudah di fuzzifikasi sebelumnya. FLR ditulis ",
        (" Ai ", "data pada hari ke t-1"),
        " → ",
        ("Aj ", "data pada hari ke t"),
    )
    flr = {
        "Tanggal": newdata[0],
        "Ai": fuzzylr[1],
        "Aj": fuzzylr[0],
        "FLR": flr,
    }
    df = pd.DataFrame(flr).set_index("Tanggal")
    st.dataframe(df, width=800, height=400)

# * Tautan ke halaman FLRG
if st.sidebar.button("FLRG"):
    annotated_text(
        annotation(
            "Fuzzy Logic Relationship Group",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahap pembentukan",
        ("Fuzzy Logic Relatationship Group", "FLRG"),
        " dilakukan dengan",
        ("FLR", ""),
        " yang mempunyai hubungan sama dikelompokkan menjadi satu hingga membentuk",
        ("FLRG", ""),
    )
    dictFLRG = {
        "CurrentState": list(flrgroup.keys()),
        "NextState": list(flrgroup.values()),
        "FLRG": list(bobot[3]),
    }
    df = pd.DataFrame(dictFLRG).set_index("CurrentState")
    st.dataframe(df, width=10000, height=400, use_container_width=True)

# * Tautan ke halaman PWMBOBOTAN
if st.sidebar.button("Pembobotan"):
    annotated_text(
        annotation(
            "Pembobotan",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahap",
        ("Pembobotan", "W"),
        " dilakukan dengan memperhatikan banyaknya relasi yang sama pada",
        ("FLRG", ""),
        ". Setelah pemberian pembobotan",
        ("FLRG", ""),
        " pada setiap relasi fuzzy, mengubah bobot FLRG menjadi",
        ("matriks pembobot", "W*"),
        " yang sudah terstandarisasi.",
    )
    dictFLRG = {
        "Kelas": list(flrgroup.keys()),
        "FLRG": bobot[3],
        "W": bobot[0],
        "W*": bobot[1],
    }
    df = pd.DataFrame(dictFLRG).set_index("Kelas")
    st.dataframe(df, width=1000, height=400, use_container_width=True)

# * Tautan ke halaman DEFUZZIFIKASI
if st.sidebar.button("Deffuzikasi"):
    annotated_text(
        annotation(
            "Defuzzifikasi",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahapan",
        (" defuzzifikasi", ""),
        " dapat dilakukan dengan mengubah ",
        ("variabel fuzzy", " linguistik"),
        " menjadi",
        ("bilangan real", ""),
        ". Tahapan ini dilakukan untuk mendapatkan ",
        ("hasil peramalan", ""),
    )

    dictDeffuzikasi = {
        "Kelas": list(deffuzikasi[0].keys()),
        "Nilai": deffuzikasi[1],
        "Deffuzikasi": list(deffuzikasi[0].values()),
    }
    df = pd.DataFrame(dictDeffuzikasi).set_index("Kelas")
    st.dataframe(df, width=1000, height=400, use_container_width=True)

# * Tautan ke halaman PERAMALAN
if st.sidebar.button("Peramalan"):
    xtanggal = [str(i) for i in newdata[0]]
    tanggal = xtanggal + ["hasil peramalan"]
    xharga = [str(i) for i in newdata[1]]
    harga = xharga + [" = "]
    xflr = [str(f"{fuzzylr[1][i]} → {fuzzylr[0][i]}") for i in range(len(fuzzylr[0]))]
    flr = xflr + [f"{fuzzylr[1][-1]} → "]
    xramalan = [str(i) for i in peramalan]
    ramalan = ["-"] + xramalan
    annotated_text(
        annotation(
            "Peramalan",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    hasilperamalan = {
        "tanggal": tanggal,
        "harga": harga,
        "flr": flr,
        "peramalan": ramalan,
    }
    df = pd.DataFrame(hasilperamalan).set_index("tanggal")
    st.dataframe(df, width=1000, height=400, use_container_width=True)


# * Tautan ke halaman MAPE
if st.sidebar.button("MAPE"):
    annotated_text(
        annotation(
            "Mean Absolute Percentage Error",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    annotated_text(
        "Tahap pengukuran ",
        ("tingkat akurasi", "%"),
        " dilakukan untuk mengetahui besar kecilnya tingkat akurasi dari hasil peramalan. Pengukuran dilakukan dengan menggunakan ",
        ("Mean Absolute Percentage Error.", "MAPE"),
        " Dalam MAPE semakin rendah nilai MAPE maka semakin baik",
        ("tingkat akurasi", "%"),
        " peramalanya.",
    )
    xtanggal = [str(i) for i in newdata[0]]
    tanggal = xtanggal + ["hasil peramalan"]
    xharga = [str(i) for i in newdata[1]]
    harga = xharga + [" = "]
    xramalan = [str(i) for i in peramalan]
    ramalan = ["-"] + xramalan
    xdifi = [str(i) for i in mape[0]]
    difi = ["-"] + xdifi + ["MAPE"]
    xdidi = [str(i) for i in mape[1]]
    didi = ["-"] + xdidi + [" = "]
    xmape = [str(f"{i} %") for i in mape[2]]
    nilaimape = ["-"] + xmape + [str(f"{mape[3]} %")]
    mapetabel = {
        "Tanggal": tanggal,
        "Harga": harga,
        "peramalan": ramalan,
        "DiFi": difi,
        "DiFi/Di": didi,
        "MAPE": nilaimape,
    }
    df = pd.DataFrame(mapetabel).set_index("Tanggal")
    st.dataframe(df, width=1000, height=400, use_container_width=True)

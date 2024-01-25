import streamlit as st
from FTSChengupdate import *
from annotated_text import annotated_text, annotation
import pandas as pd


# Judul aplikasi
st.set_page_config(page_title="FTS Cheng", page_icon="images/unej.png", layout="wide")
st.header("Implementasi Fuzzy Time Series Cheng")

# * FILTER DATA
day = st.slider("Jangka data peramalan", 1, len(dataprepocessing[0]), 1)
newdata = Filterdata(dataprepocessing, day - 1)
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
interval = Interval(round(mean), u)
panjang_interval = interval[0]
jumlah_interval = interval[1]


# * HIMPUNAN FUZZY
himpunan_fuzzy = HimpunanFuzzy(round(panjang_interval), round(jumlah_interval), u)
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


#! Tampilan ##############################################################

# * Tautan ke halaman Himpunan Semesta

if st.sidebar.button("Himpunan Semesta U"):
    b1, b2, b3 = st.columns([0.1, 0.1, 0.3])
    hs = f"""
        Dmin = {min(harga)}
        Dmax = {max(harga)}
        D1 = {d1}
        D2 = {d2}
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
        " menggunakan variabel harga dengan mencari nilai ",
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
        U= [Dmin - D1 ; Dmax  + D2 ]
        """
    )
    b1.code("Hasil", language="Python")
    b2.latex(
        f"""
        U= [ {u[0]}  ; {u[1]} ]
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
        Mean = {mean}
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
        l = {panjang_interval}
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
        p = {jumlah_interval}
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
    l = str(panjang_interval)
    p = str(jumlah_interval)

    annotated_text(
        ("himpunan fuzzy", ""),
        " dibentuk dengan membagi rentang nilai variabel sepanjang ",
        (" panjang interval", l),
        "sebanyak",
        (" jumlah interval", p),
    )
    himpunanFuzzy = {
        "Kelas": list_kelas,
        "Batas Bawah": list_bawah,
        "Batas Atas": list_atas,
        "Nilai Tengah": list_tengah,
    }
    df = pd.DataFrame(himpunanFuzzy).set_index("Kelas")
    st.dataframe(df, height=500, use_container_width=True)

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
    flr = {"Tanggal": tanggal, "Harga": harga, "Fuzzifikasi": fuzzifikasi}
    df = pd.DataFrame(flr).set_index("Tanggal")
    st.dataframe(df, height=500, use_container_width=True)

# * Tautan ke halaman FLR
if st.sidebar.button("FLR"):
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
    showflr = {"Tanggal": tanggal, "Fuzzifikasi": fuzzifikasi, "FLR (Ai → Aj)": flr}
    df = pd.DataFrame(showflr).set_index("Tanggal")
    st.dataframe(df, height=500, use_container_width=True)

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
    dictFLRG = {"Grup": grup, "Relasi": relasi, "FLRG": list(newflrg)}
    df = pd.DataFrame(dictFLRG).set_index("Grup")
    st.dataframe(df, height=500, use_container_width=True)

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
    dictFLRG = {"Grup": grup, "W": newflrg, "W*": bobot}
    df = pd.DataFrame(dictFLRG).set_index("Grup")
    st.dataframe(df, height=500, use_container_width=True)

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
        "Grup": grup,
        "Deffuzikasi": list_deffuzikasi,
        "Hasil": dict_deffuzikasi.values(),
    }
    df = pd.DataFrame(dictDeffuzikasi).set_index("Grup")
    st.dataframe(df, height=500, use_container_width=True)

# * Tautan ke halaman PERAMALAN
if st.sidebar.button("Peramalan"):
    annotated_text(
        annotation(
            "Peramalan",
            "",
            color="#EB6",
            border="2px dashed #EB6",
        )
    )
    hasilperamalan = {
        "Tanggal": tanggal + ["Hasil Peramalan"],
        "Harga": harga + [" : "],
        "FLR": flr + [f"{fuzzifikasi[-1]} →"],
        "Hasil Peramalan": [""] + peramalan,
    }
    df = pd.DataFrame(hasilperamalan).set_index("Tanggal")
    st.dataframe(df, height=500, use_container_width=True)

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
    mapetabel = {
        "Tanggal": tanggal + ["Hasil Peramalan"],
        "Harga": harga + [" : "],
        "Peramalan": [""] + peramalan,
        "DiFi": [""] + list_difi + ["Hasil MAPE"],
        "DiFi/Di": [""] + list_didi + [":"],
        "MAPE": [""] + list_mape + [nilai_mape],
    }
    df = pd.DataFrame(mapetabel).set_index("Tanggal")
    st.dataframe(df, height=500, use_container_width=True)

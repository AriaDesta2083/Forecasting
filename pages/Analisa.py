from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from controller.forecasting import Forecasting
from controller.readdata import csv_data, read_data
from controller.prepocessing import return_data
from annotated_text import annotated_text, annotation
import altair as alt
import time

#! title
st.set_page_config(
    page_title="Analisa Peramalan", page_icon="images/unej.png", layout="wide"
)

#! header

st.header(
    "Tahap Analisa Peramalan Harga Gula Pasir Lokal Tradisional Di Pasar Tradisional Indonesia"
)


#!side bar


wilayah = st.sidebar.selectbox(
    "🌏 Pilih Wilayah",
    (i for i in list(csv_data.keys())),
)
prepo = return_data(wilayah)


#! tabs

tab1, tab2, tab3 = st.tabs(["📰 DATA AKTUAL", "📈 GRAFIK DATA", "⭐FTS CHENG"])


#! tab1 Data Aktual

with tab1:
    newdata = prepo
    readdata = read_data(wilayah)[1][1:]
    dataaktual = [
        newdata[1][i] if str(newdata[1][i]) != str(readdata[i]) else "-"
        for i in range(len(newdata[1]))
    ]
    st.subheader("📰 Data Aktual")
    annotated_text(
        (f"Harga Gula Pasir Lokal", "", "color:#8B6;border:2px dashed #8B6"),
        (f"Di Pasar Tradisional", "", "color:#fea;"),
        (f"{wilayah.upper()}", "", "color:#fea;border:2px dashed #fea"),
    )
    datedata = {
        "Tanggal": newdata[0],
        "Harga": readdata,
        "Prepocessing": dataaktual,
    }
    df = pd.DataFrame(datedata).set_index("Tanggal")
    annotated_text(
        (f"{newdata[0][0].strftime('%B %Y')}", ""),
        " - ",
        (f"{newdata[0][-1].strftime('%B %Y')}", ""),
    )
    st.dataframe(df, use_container_width=True)
    st.caption(
        "NOTE : Data berikut merupakan data yang digunakan untuk melakukan analisa yang didapatkan dari Pusat Informasi Harga Pangan Strategis Nasional Kementerian Perdagangan Republik Indonesia. Data ini merupakan data aktual yang telah di prepocessing. "
    )
#! tab2 Grafik Data


def indextodate(date, tanggal):
    if date.weekday() == 5:
        date = date + timedelta(days=3)
    elif date.weekday() == 6:
        date = date + timedelta(days=2)
    else:
        date = date
    date = date.strftime("%Y-%m-%d")
    for i in range(len(tanggal)):
        if date == tanggal[i]:
            print(date, tanggal[i])
            return i


with tab2:
    tanggal, harga = prepo
    tanggal = [i.strftime("%Y-%m-%d") for i in tanggal]
    st.subheader("📈 Grafik Data")
    (txt, spc2, sl, spc3) = st.columns([3, 0.1, 4, 0.5])
    with sl.container():
        val = st.slider(
            "Rentang grafik:",
            datetime.strptime(tanggal[1], "%Y-%m-%d").date(),
            datetime.strptime(tanggal[-1], "%Y-%m-%d").date(),
            (
                datetime.strptime(tanggal[-200], "%Y-%m-%d").date(),
                datetime.strptime(tanggal[-1], "%Y-%m-%d").date(),
            ),
            format="MMM DD, YYYY",
        )
        values = (
            indextodate(val[0], tanggal),
            indextodate(val[1], tanggal),
        )

    with txt.container():
        annotated_text(
            ("Gula Pasir Lokal di pasar tradisional", "", "color:#fea;border:2px #fea"),
            " ",
            (f"{wilayah.upper()}", "", "color:#fya;border:2px dashed #fda"),
        )
        annotated_text(
            (
                f"{datetime.strptime(tanggal[values[0]], '%Y-%m-%d').strftime('%d %B %Y')}",
                "",
            ),
            " - ",
            (
                f"{datetime.strptime(tanggal[values[1]],'%Y-%m-%d').strftime('%d %B %Y')}",
                "",
            ),
        )

    source = pd.DataFrame(
        {
            "Tanggal": tanggal[values[0] : values[1] + 1],
            "Harga": harga[values[0] : values[1] + 1],
        }
    )

    # Melt data untuk membuatnya sesuai dengan format yang diinginkan oleh Altair
    source_melted = source.melt("Tanggal", var_name="category", value_name="Value")

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(
        nearest=True, on="mouseover", fields=["Tanggal"], empty=False
    )

    # The basic line
    line = (
        alt.Chart(source_melted)
        .mark_line(
            interpolate="basis",
        )
        .interactive(bind_y=True, bind_x=False)
        .encode(
            x=alt.X("Tanggal:T", title="Tanggal"),
            y=alt.Y(
                "Value:Q",
                scale=alt.Scale(
                    domain=[
                        int(min(harga)) - 1000,
                        int(max(harga)) + 1000,
                    ]
                ),
                title="Value",
            ),
            color="category:N",
        )
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart(source_melted)
        .mark_point()
        .encode(
            x="Tanggal:T",
            opacity=alt.value(0),
        )
        .add_params(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        color=alt.value("white"),
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="right", dx=5, dy=-5).encode(
        text=alt.condition(nearest, "Value:Q", alt.value(" ")),
        color=alt.value("white"),
        size=alt.value(15),
    )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(source_melted)
        .mark_rule(color="lightgrey", opacity=0.7, strokeDash=[10, 2])
        .encode(
            x="Tanggal:T",
        )
        .transform_filter(nearest)
    )

    with st.spinner("Wait for it..."):
        time.sleep(1)
        # Combine all the layers into a single char
        st.altair_chart(
            alt.layer(line, selectors, points, rules, text).properties(height=400),
            use_container_width=True,
            theme=None,
        )


#! tab3 FTS Cheng


def ftscheng(z, tahap):
    # * Tautan ke halaman Himpunan Semesta U
    if "Himpunan Semesta U" in tahap:
        b1, b2, b3 = st.columns([0.1, 0.1, 0.3])
        hs = f"""
            Dmin = {min(z.harga)}
            Dmax = {max(z.harga)}
            D1 = {abs(z.u[0]-min(z.harga))}
            D2 = {abs(max(z.harga)-z.u[1])}
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
            U= [ {z.u[0]}  ; {z.u[1]} ]
        """
        )

    # * Tautan ke halaman Interval Fuzzy

    if "Interval Average" in tahap:
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
            Mean = {z.mean}
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
            l = {z.panjang_interval}
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
            p = {z.jumlah_interval}
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

    if "Himpunan Fuzzy" in tahap:
        annotated_text(
            annotation(
                "Himpunan Fuzzy",
                "",
                color="#EB6",
                border="2px dashed #EB6",
            )
        )
        l = str(z.panjang_interval)
        p = str(z.jumlah_interval)

        annotated_text(
            ("himpunan fuzzy", ""),
            " dibentuk dengan membagi rentang nilai variabel sepanjang ",
            (" panjang interval", l),
            "sebanyak",
            (" jumlah interval", p),
        )
        himpunanFuzzy = {
            "Kelas": z.list_kelas,
            "Batas Bawah": z.list_bawah,
            "Batas Atas": z.list_atas,
            "Nilai Tengah": z.list_tengah,
        }
        df = pd.DataFrame(himpunanFuzzy).set_index("Kelas")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman Fuzzifikasi

    if "Fuzzifikasi" in tahap:
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
        df_flr = {"Tanggal": z.tanggal, "Harga": z.harga, "Fuzzifikasi": z.fuzzifikasi}
        df = pd.DataFrame(df_flr).set_index("Tanggal")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman FLR

    if "Fuzzy Logic Relationship" in tahap:
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
        showflr = {
            "Tanggal": z.tanggal,
            "Fuzzifikasi": z.fuzzifikasi,
            "FLR (Ai → Aj)": z.flr,
        }
        df = pd.DataFrame(showflr).set_index("Tanggal")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman FLRG

    if "FLR Group" in tahap:
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
        dictFLRG = {"Grup": z.grup, "Relasi": z.relasi, "FLRG": list(z.newflrg)}
        df = pd.DataFrame(dictFLRG).set_index("Grup")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman PWMBOBOTAN

    if "Pembobotan" in tahap:
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
        dictFLRG = {"Grup": z.grup, "W": z.newflrg, "W*": z.bobot}
        df = pd.DataFrame(dictFLRG).set_index("Grup")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman DEFUZZIFIKASI

    if "Defuzzifikasi" in tahap:
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
            "Grup": z.grup,
            "Deffuzikasi": z.list_defuzzifikasi,
            "Hasil": z.dict_defuzzifikasi.values(),
        }
        df = pd.DataFrame(dictDeffuzikasi).set_index("Grup")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman PERAMALAN

    if "Peramalan" in tahap:
        annotated_text(
            annotation(
                "Peramalan",
                "",
                color="#EB6",
                border="2px dashed #EB6",
            )
        )
        annotated_text(
            "Tahap",
            ("Peramalan", ""),
            " dilakukan dengan menggunakan nilai setiap kelas defuzzifikasi yang telah dihitung sebelumnya.",
        )
        hasilperamalan = {
            "Tanggal": z.tanggal + ["Hasil Peramalan"],
            "Harga": z.harga + [" : "],
            "FLR": z.flr + [f"{z.fuzzifikasi[-1]} →"],
            "Hasil Peramalan": [""] + z.peramalan,
        }
        df = pd.DataFrame(hasilperamalan).set_index("Tanggal")
        st.dataframe(df, height=500, use_container_width=True)

    # * Tautan ke halaman MAPE

    if "Mean Absolute Percentage Error" in tahap:
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
            "Tanggal": z.tanggal + ["Hasil Peramalan"],
            "Harga": z.harga + [" : "],
            "Peramalan": [""] + z.peramalan,
            "DiFi": [""] + z.list_difi + ["Hasil MAPE"],
            "DiFi/Di": [""] + ["{:.5f}".format(i) for i in z.list_didi] + [":"],
            "MAPE(%)": [""]
            + [str(i) + " %" for i in z.list_mape]
            + [str(z.nilai_mape) + " %"],
        }
        df = pd.DataFrame(mapetabel).set_index("Tanggal")
        st.dataframe(df, height=500, use_container_width=True)

    else:
        pass


with tab3:
    st.subheader("Fuzzy Time Series Cheng")
    tahap = st.selectbox(
        f"Berikut merupakan dokumentasi tahap - tahap peramalan harga gula pasir lokal dipasar tradisional {wilayah.upper()} menggunakan metode FTS Cheng ",
        (
            "Himpunan Semesta U",
            "Interval Average",
            "Himpunan Fuzzy",
            "Fuzzy Logic Relationship",
            "FLR Group",
            "Pembobotan",
            "Defuzzifikasi",
            "Peramalan",
            "Mean Absolute Percentage Error",
        ),
    )
    with st.spinner("Wait for it..."):
        time.sleep(1)
        z = Forecasting(prepo)
        ftscheng(z, tahap)

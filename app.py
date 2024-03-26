import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages
from annotated_text import annotated_text
from controller.readdata import csv_data
from controller.prepocessing import return_data
from controller.build import build_forecast, prediksi
from datetime import datetime, timedelta
import locale
import time
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Hasil Peramalan", page_icon="images/unej.png", layout="wide"
)

show_pages(
    [
        Page("app.py", "Hasil Peramalan", "🔍"),
        Page("pages/Analisa.py", "Analisa Peramalan", "📚"),
    ]
)


wilayah = st.sidebar.selectbox(
    "🌏 Pilih Wilayah",
    (i for i in list(csv_data.keys())),
)

#! import data

tanggal_peramalan, jumlah_peramalan, z = build_forecast(return_data(wilayah))
az = prediksi(z.harga, tanggal_peramalan, jumlah_peramalan)


st.header("Peramalan Harga Gula Pasir Lokal Tradisional Di Pasar Tradisional Indonesia")

tab1, tab2 = st.tabs(["💵 HASIL PERAMALAN", "📈 GRAFIK PERAMALAN"])


#! HASIL PERAMALAN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
with tab1:
    annotated_text(
        "Hasil peramalan harga ",
        ("gula pasir lokal 💵 ", "", "color:#8B6;border:2px dashed #8B6"),
        " di pasar tradisional ",
        (f"{wilayah.upper()} 📍 ", "", "color:#fea;border:2px dashed #fea"),
    )

    # Atur locale ke Indonesia
    locale.setlocale(locale.LC_ALL, "id_ID")

    kemarin = datetime.strptime(az.tanggal[-3], "%Y-%m-%d")
    hari_ini = datetime.strptime(az.tanggal[-2], "%Y-%m-%d")
    besok = datetime.strptime(az.tanggal[-1], "%Y-%m-%d")

    st.markdown(
        """
        <style>
            .custom-container {
                border: 2px solid #e1e1e1;
                border-radius: 10px;
                padding: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Membuat container

    with st.spinner("Wait for it..."):
        time.sleep(1)
        col1, cols, col2, cola, col3 = st.columns([5, 1, 5, 1, 5])
        col1.code(
            "Kemarin",
            language="python",
        )
        col1.metric(
            f"{kemarin.strftime('%A, %d %b %Y')} ",
            f"{locale.currency(az.peramalan[-3], grouping=True)}",
            f"{az.peramalan[-3] - az.peramalan[-4]}",
        )

        col2.code("Hari ini", language="python")
        col2.metric(
            f"{hari_ini.strftime('%A, %d %b %Y')}",
            f"{locale.currency(az.peramalan[-2], grouping=True)}",
            f"{az.peramalan[-2] - az.peramalan[-3]}",
        )

        col3.code("Besok", language="python")
        col3.metric(
            f"{besok.strftime('%A, %d %b %Y')}",
            f"{locale.currency(az.peramalan[-1], grouping=True)}",
            f"{az.peramalan[-1] - az.peramalan[-2]}",
        )

st.write()


#! GRAFIK PERAMALAN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


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
    (txt, sl, spc3) = st.columns([3, 4, 1])
    with sl.container():
        val = st.slider(
            "📅 Rentang grafik :",
            datetime.strptime(az.tanggal[1], "%Y-%m-%d").date(),
            datetime.strptime(az.tanggal[-1], "%Y-%m-%d").date(),
            (
                datetime.strptime(az.tanggal[-200], "%Y-%m-%d").date(),
                datetime.strptime(az.tanggal[-1], "%Y-%m-%d").date(),
            ),
            format="MMM DD, YYYY",
        )
        values = (
            indextodate(val[0], az.tanggal),
            indextodate(val[1], az.tanggal),
        )

    with txt.container():
        annotated_text(
            ("📈 GRAFIK PERAMALAN", "", "color:#fea;border:2px #fea"),
            " ",
            (f"{wilayah.upper()} 📍 ", "", "color:#fya;border:2px dashed #fda"),
        )
        annotated_text(
            (
                f"{datetime.strptime(az.tanggal[values[0]], '%Y-%m-%d').strftime('%d %B %Y')}",
                "",
            ),
            " - ",
            (
                f"{datetime.strptime(az.tanggal[values[1]],'%Y-%m-%d').strftime('%d %B %Y')}",
                "",
            ),
        )

    source = pd.DataFrame(
        {
            "Tanggal": az.tanggal[values[0] : values[1] + 1],
            "Harga": az.harga[values[0] : values[1] + 1],
            "Peramalan": az.peramalan[values[0] : values[1] + 1],
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
                        int(min(source["Peramalan"])) - 1000,
                        int(max(source["Peramalan"])) + 1000,
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

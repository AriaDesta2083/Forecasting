import streamlit as st
from st_pages import Page, show_pages
from annotated_text import annotated_text
from controller.forecasting import Forecasting
from controller.prepocessing import *
from controller.api import *
from controller.build import build_forecast
from datetime import date, datetime, timedelta
import locale
import time
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Hasil Peramalan",
    page_icon="images/unej.png",
    layout="wide",
    menu_items={
        "report a bug": "https://www.instagram.com/ariadestap/ ",
        "about": "GitHub : https://github.com/AriaDesta2083",
    },
)

show_pages(
    [
        Page("app.py", "Hasil Peramalan", "🔍"),
        Page("pages/Analisa.py", "Analisa Peramalan", "📚"),
    ]
)

st.header("Peramalan Harga Gula Pasir Lokal Tradisional Di Pasar Tradisional Indonesia")

tab1, tab2 = st.tabs(["💵 HASIL PERAMALAN", "📈 GRAFIK PERAMALAN"])

# #! import data with data api
# end_date = date(2024, 4, 4)
end_date = date.today()
start_date = end_date - timedelta(days=360 * 3)
prov_dict = get_list_wilayah()
list_prov = ["Indonesia"] + list(prov_dict.keys())
prov = st.sidebar.selectbox(
    "🌏 Pilih Wilayah",
    (i for i in list_prov),
)
id_prov = prov_dict.get(prov)
data, tanggal, harga = get_api(id_prov if id_prov else "", end_date, start_date)


#! melakukan peramalan

z = Forecasting(prepocessing((tanggal, harga)))
tanggal, harga, peramalan = build_forecast(z)


#! HASIL PERAMALAN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
wilayah = prov
with tab1:
    annotated_text(
        "Hasil peramalan harga ",
        ("gula pasir lokal 💵 ", " per kilogram ", "color:#8B6;border:2px dashed #8B6"),
        " di pasar tradisional ",
        (f"{wilayah.upper()} 📍 ", "", "color:#fea;border:2px dashed #fea"),
    )

    # Atur locale ke Indonesia
    locale.setlocale(locale.LC_ALL, "id_ID")

    index = -2
    # kemarin = datetime.strptime(str(tanggal[index - 1]), "%Y-%m-%d")
    # hari_ini = datetime.strptime(str(tanggal[index]), "%Y-%m-%d")
    # besok = datetime.strptime(str(tanggal[index + 1]), "%Y-%m-%d")
    kemarin = tanggal[index - 1]
    hari_ini = tanggal[index]
    besok = tanggal[index + 1]

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
            f"{locale.currency(harga[index-1], grouping=True)}",
            f"{harga[index-1] - harga[index-2]}",
        )

        col2.code("Hari ini", language="python")
        col2.metric(
            f"{hari_ini.strftime('%A, %d %b %Y')}",
            f"{locale.currency(harga[index], grouping=True)}",
            f"{harga[index] - harga[index-1]}",
        )

        col3.code("Besok", language="python")
        col3.metric(
            f"{besok.strftime('%A, %d %b %Y')}",
            f"{locale.currency(peramalan[index+1], grouping=True)}",
            f"{peramalan[index+1] - harga[index]}",
        )
        st.caption(
            f"Note : Harga gula diatas merupakan hasil peramalan harga per kilogram jenis gula pasir lokal di pasar tradisional di {wilayah}."
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
    for i in range(len(tanggal)):
        if date == tanggal[i]:
            return i


with tab2:
    (txt, sl, spc3) = st.columns([3, 4, 1])
    with sl.container():
        val = st.slider(
            "📅 Rentang grafik :",
            tanggal[1],
            tanggal[-1],
            (
                tanggal[-200],
                tanggal[-1],
            ),
            format="MMM DD, YYYY",
        )
        values = (
            indextodate(val[0], tanggal),
            indextodate(val[1], tanggal),
        )

    with txt.container():
        annotated_text(
            ("📈 GRAFIK PERAMALAN", "", "color:#fea;border:2px #fea"),
            " ",
            (f"{wilayah.upper()} 📍 ", "", "color:#fya;border:2px dashed #fda"),
        )
        annotated_text(
            (
                f"{tanggal[values[0]]}",
                "",
            ),
            " - ",
            (
                f"{tanggal[values[1]]}",
                "",
            ),
        )

    source = pd.DataFrame(
        {
            "Tanggal": tanggal[values[0] : values[1] + 1],
            "Harga": harga[values[0] : values[1] + 1],
            "Peramalan": peramalan[values[0] : values[1] + 1],
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
        text=alt.condition(nearest, "Value:Q", alt.value("")),
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

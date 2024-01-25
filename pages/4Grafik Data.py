import numpy as np
import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from FTSChengupdate import *
import altair as alt


st.set_page_config(page_title="Grafik Data", page_icon="images/unej.png", layout="wide")


def PlotMonth(dates, prices):
    # * Membuat kamus defaultdict untuk menyimpan harga-harga per bulan dan tahun
    prices_per_month_year = defaultdict(int)
    count_per_month_year = defaultdict(int)

    # * Mengelompokkan harga-harga per bulan dan tahun dan menghitung jumlah data per bulan dan tahun
    for date, price in zip(dates, prices):
        month_year = date.strftime("%Y-%m")
        prices_per_month_year[month_year] += price
        count_per_month_year[month_year] += 1

    # * Membuat array tanggal baru dan array harga baru
    new_dates = []
    new_prices = []

    # * Mengisi array tanggal baru dan array harga baru dengan nilai rata-rata per bulan dan tahun
    for month_year, price_sum in prices_per_month_year.items():
        count = count_per_month_year[month_year]
        average_price = price_sum / count
        new_dates.append(month_year)
        new_prices.append(int(round(average_price)))

    return new_dates, new_prices


st.header("GRAFIK HARGA")
annotated_text(
    "Grafik harga ",
    ("gula pasir lokal", "", "color:#8B6;border:2px dashed #8B6"),
    " di pasar tradisional ",
    (" Indonesia", "", "color:#fea;border:2px dashed #fea"),
)

newdata = Filterdata(dataprepocessing, 0)
semesta = SemestaU(newdata[1])

dmin = semesta[0][0]
dmax = semesta[0][1]

monthdata = PlotMonth(newdata[0], newdata[1])
# Membuat slider untuk mengatur zoom grafik
tanggal = newdata[0]
harga = newdata[1]


agree = st.sidebar.checkbox("Grafik data rata rata perbulan")

if agree:
    tanggal = monthdata[0]
    harga = monthdata[1]


option_interpolate = st.sidebar.selectbox(
    "Pilih bentuk line chart",
    (
        "basis",
        "bundle",
        "cardinal",
        "catmull-rom",
        "linear",
        "monotone",
        "natural",
        "step",
    ),
)


values = st.slider(
    "Range data",
    0,
    len(tanggal) - 1,
    (0, len(tanggal) - 1),
)

annotated_text(("Range data", ""), " : ", (str(values[1] - values[0]), "data"))
annotated_text((str(tanggal[values[0]]), ""), " - ", (str(tanggal[values[1]]), ""))


dataframe = pd.DataFrame(
    {
        "tanggal": tanggal[values[0] : values[1] + 1],
        "harga": harga[values[0] : values[1] + 1],
    }
)
nearest = alt.selection_point(
    nearest=True, on="mouseover", fields=["tanggal"], empty=False
)


chartaltair = (
    alt.Chart(dataframe)
    .mark_line(
        clip=True,
        color="orangered",
        opacity=0.8,
        interpolate=option_interpolate,
    )
    .interactive(bind_y=True, bind_x=False)
    .encode(
        x=alt.X("tanggal", title="Tanggal"),
        y=alt.Y(
            "harga",
            scale=alt.Scale(domain=[dmin, dmax]),
            title="Harga",
        ),
    )
    .properties(height=450)
)

selectors = (
    alt.Chart(dataframe)
    .mark_point()
    .encode(
        x="tanggal",
        opacity=alt.value(0),
    )
    .add_params(nearest)
)

# Draw points on the line, and highlight based on selection
points = chartaltair.mark_point().encode(
    color=alt.value("white"),
    opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
)

# Draw text labels near the points, and highlight based on selection
text = chartaltair.mark_text(align="left", dx=5, dy=-5, style="italic").encode(
    text=alt.condition(nearest, "harga:Q", alt.value(" ")),
    color=alt.value("white"),
    size=alt.value(16),
)

# Draw a rule at the location of the selection
rules = (
    alt.Chart(dataframe)
    .mark_rule(color="lightgrey", opacity=0.7, strokeDash=[10, 2])
    .encode(
        x="tanggal",
    )
    .transform_filter(nearest)
)


st.altair_chart(
    alt.layer(chartaltair, selectors, points, rules, text).properties(height=500),
    theme=None,
    use_container_width=True,
)


# Menampilkan grafik Altair di Streamlit


# chart_data = pd.DataFrame(harga, tanggal)
# # Mengonversi tipe data elemen-elemen dalam list menjadi string
# data_gabungan = list(
#     map(
#         lambda x: list(map(str, x)),
#         (zip(tanggal[0:20], harga[0:20], harga[20:40])),
#     )
# )
# dfbarchart = pd.DataFrame(data_gabungan, columns=["model", "HargaLama", "HargaBaru"])
# source = pd.melt(dfbarchart, id_vars=["model"])

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# c = (
#     alt.Chart(chart_data)
#     .mark_circle()
#     .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
# )

# st.altair_chart(c, use_container_width=True)

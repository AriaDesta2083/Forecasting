import time
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from build import *
from annotated_text import annotated_text

st.set_page_config(
    page_title="Grafik Peramalan", page_icon="images/unej.png", layout="wide"
)

tanggal = new_tanggal
harga = new_harga
peramalan = new_peramalan
dmin = min(harga)
dmax = max(harga)

st.header("GRAFIK PERAMALAN HARGA GULA")
annotated_text(
    "Grafik peramalan harga ",
    ("gula pasir lokal", "", "color:#8B6;border:2px dashed #8B6"),
    " di pasar tradisional ",
    (" Indonesia", "", "color:#fea;border:2px dashed #fea"),
)

values = st.slider(
    "Range data",
    0,
    len(tanggal) - 1,
    (0, len(tanggal) - 1),
)


annotated_text(("Range data", ""), " : ", (str(values[1] - values[0]), "data"))
annotated_text((str(tanggal[values[0]]), ""), " - ", (str(tanggal[values[1]]), ""))


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
    .mark_line(interpolate="basis")
    .interactive(bind_y=True, bind_x=False)
    .encode(
        x=alt.X("Tanggal:T", title="Tanggal"),
        y=alt.Y(
            "Value:Q",
            scale=alt.Scale(domain=[dmin - 1000, dmax + 1000]),
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
    time.sleep(3)
    # Combine all the layers into a single char
    st.altair_chart(
        alt.layer(line, selectors, points, rules, text).properties(height=600),
        use_container_width=True,
        theme=None,
    )

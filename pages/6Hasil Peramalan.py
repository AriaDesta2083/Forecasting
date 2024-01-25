import streamlit as st
from annotated_text import annotated_text
from build import *
import locale

st.set_page_config(
    page_title="Hasil Peramalan", page_icon="images/unej.png", layout="wide"
)

st.header("HASIL PERAMALAN HARGA GULA")
annotated_text(
    "Hasil peramalan harga ",
    ("gula pasir lokal", "", "color:#8B6;border:2px dashed #8B6"),
    " di pasar tradisional ",
    (" Indonesia", "", "color:#fea;border:2px dashed #fea"),
)


# Atur locale ke Indonesia
locale.setlocale(locale.LC_ALL, "id_ID")

kemarin = datetime.strptime(new_tanggal[-3], "%Y-%m-%d")
hari_ini = datetime.strptime(new_tanggal[-2], "%Y-%m-%d")
besok = datetime.strptime(new_tanggal[-1], "%Y-%m-%d")

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
container = st.container()
col1, cols, col2, cola, col3 = st.columns([5, 1, 5, 1, 5])
with st.container():
    col1.code("Kemarin", language="python")
    col1.metric(
        f"{kemarin.strftime('%A, %d %b %Y')} ",
        f"{locale.currency(new_peramalan[-3], grouping=True)}",
        f"{new_peramalan[-3] - new_peramalan[-4]}",
    )

    col2.code("Hari ini")
    col2.metric(
        f"{hari_ini.strftime('%A, %d %b %Y')}",
        f"{locale.currency(new_peramalan[-2], grouping=True)}",
        f"{new_peramalan[-2] - new_peramalan[-3]}",
    )

    col3.code("Besok")
    col3.metric(
        f"{besok.strftime('%A, %d %b %Y')}",
        f"{locale.currency(new_peramalan[-1], grouping=True)}",
        f"{new_peramalan[-1] - new_peramalan[-2]}",
    )

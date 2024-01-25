import streamlit as st
import time
import numpy as np
from FTSChengupdate import *
import pandas as pd
from annotated_text import annotated_text

st.set_page_config(page_title="Data Aktual", page_icon="images/unej.png")

st.header("DATA HARGA GULA")
annotated_text(
    "Data harga ",
    ("gula pasir lokal", "", "color:#8B6;border:2px dashed #8B6"),
    " di pasar tradisional ",
    (" Indonesia", "", "color:#fea;border:2px dashed #fea"),
)
annotated_text(("Januari 2021", ""), " - ", ("Desember 2023", ""))

newdata = Filterdata(dataprepocessing, 0)

datedata = {"Tanggal": newdata[0], "Harga": newdata[1]}
df = pd.DataFrame(datedata).set_index("Tanggal")


# Fungsi pencarian berdasarkan harga
def search_by_price(price):
    result = df[df["Harga"] == price]
    return result


# Fungsi pencarian berdasarkan tanggal
def search_by_date(date):
    result = df[df.index == date]
    return result


with st.spinner("Wait for it..."):
    time.sleep(1)

st.dataframe(df, height=500, use_container_width=True)

search_option = st.selectbox(
    "Pilih opsi pencarian:", ["Harga", "Tanggal"], key="search_option"
)
# Input dari pengguna untuk pencarian
result = None

if search_option == "Harga":
    search_value = st.text_input(
        "Masukkan harga pencarian:",
        key="search_value",
    )
elif search_option == "Tanggal":
    search_value = st.date_input("Masukkan tanggal pencarian:", key="search_value")

if search_option == "Harga":
    if search_value != "":
        result = search_by_price(int(search_value))
elif search_option == "Tanggal":
    if search_value != None:
        date = search_value
        result = search_by_date(date)
else:
    result = None

if result is not None and not result.empty:
    st.subheader("Hasil Pencarian:")
    st.table(result)
elif result is None:
    st.write("  ")
else:
    st.write("Tidak ada hasil pencarian yang cocok.")

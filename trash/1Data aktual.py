import streamlit as st
import time
import numpy as np
from FTSCheng import newdata
import pandas as pd
from annotated_text import annotated_text, annotation

st.set_page_config(page_title="Data Aktual", page_icon="images/unej.png")

st.header("Data Aktual")
annotated_text(
    "Data harga ",
    ("gula pasir lokal", "", "color:#8B6;border:2px dashed #8B6"),
    " di pasar tradisional ",
    (" Indonesia", "", "color:#fea;border:2px dashed #fea"),
)
annotated_text(("Januari 2021", ""), " - ", ("Desember 2023", ""))
# Data harga dan tanggal

datedata = {"Tanggal": newdata[0], "Harga": newdata[1]}

# Membuat dataframe dari data
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

st.dataframe(df, width=800, height=300)

search_option = st.selectbox(
    "Pilih opsi pencarian:", ["Harga", "Tanggal"], key="search_option"
)
result = None
# Input dari pengguna untuk pencarian
if search_option == "Harga":
    search_value = st.text_input("Masukkan nilai pencarian harga:", key="search_value")
elif search_option == "Tanggal":
    search_value = st.date_input("Masukkan tanggal pencarian:", key="search_value")
# Melakukan pencarian berdasarkan opsi yang dipilih
result = None
if search_option == "Harga":
    if search_value != "":
        result = search_by_price(int(search_value))
elif search_option == "Tanggal":
    if search_value != None:
        date = search_value
        result = search_by_date(date)
else:
    result = None
# Menampilkan hasil pencarian
if result is not None and not result.empty:
    st.subheader("Hasil Pencarian:")
    st.table(result)
else:
    st.write("Tidak ada hasil pencarian yang cocok.")


# active_tab = st.sidebar.selectbox("Data berdasarkan", ["🗃 Hari", "🗃 Bulan"])

# if active_tab == "🗃 Hari":
#     # st.subheader("HARI")

# def search_by_price2(price):
#     result = df2[df2["Harga"] == price]
#     return result

# def search_by_date2(date):
#     result = df2[df2.index == date]
#     return result


# elif active_tab == "🗃 Bulan":
#     st.subheader("BULAN")
#     st.dataframe(df2, width=1000, height=300)
#     # Input dari pengguna untuk pencarian
#     search_option2 = st.selectbox(
#         "Pilih opsi pencarian:", ["Harga", "Tanggal"], key="search_option2"
#     )
#     result = None
#     if search_option2 == "Harga":
#         search_value2 = st.text_input(
#             "Masukkan nilai pencarian harga:", key="search_value2"
#         )
#     elif search_option2 == "Tanggal":
#         search_value2 = st.date_input(
#             "Masukkan tanggal pencarian:", key="search_value2"
#         )
#     if search_option2 == "Harga":
#         if search_value2 != "":
#             result = search_by_price2(int(search_value2))
#     elif search_option2 == "Tanggal":
#         if search_value2 != None:
#             date = search_value2
#             date = date.strftime("%Y-%m")
#             result = search_by_date2(date)
#     else:
#         result = None
#     # Menampilkan hasil pencarian
#     if result is not None and not result.empty:
#         st.subheader("Hasil Pencarian:")
#         st.table(result)
#     else:
#         st.write("Tidak ada hasil pencarian yang cocok.")

# else:
#     st.write("cde")

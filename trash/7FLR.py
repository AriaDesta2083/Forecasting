import streamlit as st
import pandas as pd
from trash.FTSCheng import newdata, fuzzylr

# from FTSCheng import hFuzzy

st.set_page_config(page_title="FLR", page_icon="images/unej.png")
st.header("Fuzzy Logic Relationships")
flr = {
    "Tanggal": newdata[0],
    "Harga": newdata[1],
    "Fuzzifikasi": fuzzylr[0],
    "FLR": fuzzylr[1],
}

df = pd.DataFrame(flr).set_index("Tanggal")
st.dataframe(df, width=800, height=300)

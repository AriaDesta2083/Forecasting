import streamlit as st
import pandas as pd
from trash.FTSCheng import hFuzzy

st.set_page_config(page_title="himpunan fuzzy", page_icon="images/unej.png")
st.header("Himpunan Fuzzy")
himpunanFuzzy = {
    "Kelas": hFuzzy[0],
    "Batas Bawah": hFuzzy[1],
    "Batas Atas": hFuzzy[2],
    "Nilai Tengah": hFuzzy[3],
}
df = pd.DataFrame(himpunanFuzzy).set_index("Kelas")
st.dataframe(df, width=800, height=600)

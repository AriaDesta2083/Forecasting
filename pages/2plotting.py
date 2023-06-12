from datetime import datetime
import streamlit as st
import time
import numpy as np
from FTSCheng import newdata,monthdata
import pandas as pd

if "boolean" not in st.session_state:
    st.session_state.boolean = False

st.set_page_config(page_title="Plotting", page_icon="images/unej.png")
seesion = st.session_state.boolean
st.markdown("# Plotting")
st.sidebar.header("Harga Gula Pasir Lokal")
st.write(
    """Plotting Harga Gula Pasir Lokal  Mei 2018 - Mei 2023 di Indonesia   """
)

rerun_button = st.button("Reload")
if rerun_button:
    st.session_state.boolean = True
    st.experimental_rerun()

tanggal = newdata[0]
harga = newdata[1]
status = st.sidebar.text('Berdasarkan Hari')
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
tanggal2 = monthdata[0][1:len(monthdata[0])-1]
harga2 = monthdata[1][1:len(monthdata[1])-1]
status = st.sidebar.text('Berdasarkan Bulan')
progress_bar2 = st.sidebar.progress(0)
status_text2 = st.sidebar.empty()
if seesion:
    st.markdown("### Berdasarkan Hari")
    chart = st.line_chart(pd.DataFrame(harga[0:1],tanggal[0:1]))
    for i in range(len(harga)):
        status_text.text(str(i+1)+" / "+str(len(harga))+" Complete")
        chart.add_rows(pd.DataFrame([harga[i]],[tanggal[i]]))
        progress_bar.progress((i+1)/len(harga))
        time.sleep(0.05)
    if seesion:
        st.success("Data Hari Done")
    time.sleep(5)
    st.markdown("### Berdasarkan Bulan")
    chart2 = st.line_chart(pd.DataFrame(harga2[0:1],tanggal2[0:1]))
    for i in range(len(harga2)):
        status_text2.text(str(i+1)+" / "+str(len(harga2))+" Complete")
        chart2.add_rows(pd.DataFrame([harga2[i]],[tanggal2[i]]))
        progress_bar2.progress((i+1)/len(harga2))
        time.sleep(0.5)
    if seesion:
        st.success("Data Bulan Done")
    st.session_state.boolean = False

else:
    st.markdown("### Berdasarkan Hari")
    chart = st.line_chart(pd.DataFrame(harga,tanggal))
    st.markdown("### Berdasarkan Bulan")
    chart2 = st.line_chart(pd.DataFrame(harga2,tanggal2))
    
progress_bar.empty()
progress_bar2.empty()
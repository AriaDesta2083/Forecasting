from datetime import datetime
import streamlit as st
import time
import numpy as np
from trash.FTSCheng import newdata, monthdata, round_thousand
import pandas as pd

if "boolean" not in st.session_state:
    st.session_state.boolean = False

st.set_page_config(page_title="Plotting", page_icon="images/unej.png")
seesion = st.session_state.boolean
st.markdown("# Plotting")
st.sidebar.header("Harga Gula Pasir Lokal")
st.write("""Plotting Harga Gula Pasir Lokal  Mei 2018 - Mei 2023 di Indonesia   """)

# def round_thousand(harga):
#     return (harga//1000)*1000

rerun_button = st.button("Reload")
if rerun_button:
    st.session_state.boolean = False
    st.experimental_rerun()


# tanggal = [datetime.strftime(x,'%d/%m/%Y') for x in newdata[0]]
tanggal = newdata[0]
harga = newdata[1]
status = st.sidebar.text("Berdasarkan Hari")
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

tanggal2 = monthdata[0][1 : len(monthdata[0]) - 1]
harga2 = monthdata[1][1 : len(monthdata[1]) - 1]
status = st.sidebar.text("Berdasarkan Bulan")
progress_bar2 = st.sidebar.progress(0)
status_text2 = st.sidebar.empty()


def create_trendline(data):
    x = np.arange(len(data))
    y = data
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    trendline = p(x)
    return trendline


def prepocessing(harga):
    minharga = min(harga)
    maxharga = max(harga)
    newmaxharga = maxharga + 150
    newminharga = minharga - 50
    for i in range(len(harga)):
        if np.isnan(harga[i]):
            pre = (harga[i - 1] - minharga) / (maxharga - minharga) * (
                newmaxharga - newminharga
            ) + newminharga
            harga[i] = round(int(pre))
    newharga = harga
    return newharga


def pre_component(data, date):
    # index = []
    # *COVID
    datecovid = ["2019-12", "2020-09"]
    indexcovid = [i for i in range(len(date)) if date[i] in datecovid]
    covid = [np.nan for _ in range(len(data))]
    covid[int(indexcovid[0]) : int(indexcovid[1]) + 1] = [
        data[i] for i in range((indexcovid[0]), int(indexcovid[1]) + 1)
    ]
    # *Membuat data baru dengan menghiraukan data COVID
    newdata = [data[i] for i in range(len(data))]
    # *in here
    newdata[int(indexcovid[0]) : int(indexcovid[1]) + 1] = [
        np.nan for i in range((indexcovid[0]), int(indexcovid[1]) + 1)
    ]
    newcovid = prepocessing(newdata)
    return newcovid, covid


def titik_minmax(data):
    index = []
    if data[0] > data[1]:
        count = True
    else:
        count = False
    for i in range(len(data) - 1):
        if count:
            if data[i] > data[i + 1]:
                index.append(i)
                count = False
        else:
            if data[i] < data[i + 1]:
                index.append(i)
                count = True
    index = [data[i] if i in index else np.nan for i in range(len(data))]
    return index


def titik_ramadhan(date, value):
    ramadhan = ["2018-05", "2019-05", "2020-04", "2021-04", "2022-04", "2022-03"]
    index = []
    for i in range(len(date) - 1):
        if date[i] in ramadhan:
            index.append(i - 3)
            index.append(i - 2)
            index.append(i - 1)
            index.append(i)
    musim = [value[i] if i in index else np.nan for i in range(len(date))]
    return musim


if seesion:
    st.markdown("### Berdasarkan Hari")
    chart = st.line_chart(pd.DataFrame(harga[0:1], tanggal[0:1]))
    for i in range(len(harga)):
        status_text.text(str(i + 1) + " / " + str(len(harga)) + " Complete")
        chart.add_rows(pd.DataFrame([harga[i]], [tanggal[i]]))
        progress_bar.progress((i + 1) / len(harga))
        time.sleep(0.05)
    if seesion:
        st.success("Data Hari Done")

    time.sleep(5)

    st.markdown("### Berdasarkan Bulan")
    chart2 = st.line_chart(pd.DataFrame(harga2[0:1], tanggal2[0:1]))
    for i in range(len(harga2)):
        status_text2.text(str(i + 1) + " / " + str(len(harga2)) + " Complete")
        chart2.add_rows(pd.DataFrame([harga2[i]], [tanggal2[i]]))
        progress_bar2.progress((i + 1) / len(harga2))
        time.sleep(0.5)

else:
    # * component hari
    trendday = create_trendline(harga)
    st.markdown("### Berdasarkan Hari")
    dataday = pd.DataFrame(
        {
            "trendline": trendday,
            "harga": harga,
            "month": tanggal,
        }
    )
    chart = st.line_chart(dataday.set_index("month"))

    # * component bulan
    st.markdown("### Berdasarkan Bulan")
    monthcomp = pre_component(harga2, tanggal2)
    trendmonth = create_trendline(monthcomp[0])
    covid = monthcomp[1]
    newcovid = monthcomp[0]
    #! titik = titik_minmax(harga2)
    titik = titik_ramadhan(tanggal2, harga2)
    datamounth = pd.DataFrame(
        {"harga": harga2, "covid": covid, "titik": titik, "month": tanggal2}
    )
    chart2 = st.line_chart(datamounth.set_index("month"))
# progress_bar.empty()
# progress_bar2.empty()

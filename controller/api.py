import requests
import streamlit as st


@st.cache_data(show_spinner="Fetching data from API...", max_entries=1000, ttl=3600 * 5)
def get_list_wilayah():
    get_list_prov = requests.get(
        "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetRefProvince?"
    )
    list_prov = get_list_prov.json()
    provinsi_dict = {item["name"]: item["id"] for item in list_prov["data"]}
    return provinsi_dict


def build_api(id_wilayah, end_date, start_date):
    # Get data provinsi
    start = start_date.strftime("%Y/%m/%d")
    end = end_date.strftime("%Y/%m/%d")
    # Build URL
    base_url = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataDaerah"
    url = f"{base_url}?price_type_id=1&comcat_id=com_21&province_id={id_wilayah}&regency_id=&market_id=&tipe_laporan=1&start_date={start}&end_date={end}"
    return url


def fetchdata(data):
    tanggal = []
    harga = []
    for key, value in data.items():
        if key not in ["no", "name", "level"]:
            harga.append(value.replace(",", ""))
            tanggal.append(key)
        else:
            pass
    if harga[-1] == "-":
        return tanggal[:-1], harga[:-1]
    else:
        return tanggal, harga


@st.cache_data(show_spinner="Fetching data from API...", max_entries=1000, ttl=3600 * 5)
def get_api(id_wilayah, start_date, end_date):
    go = build_api(id_wilayah, start_date, end_date)
    response = requests.get(go)
    if response.status_code == 200:
        try:
            data = response.json()["data"][1]
            if data:
                tanggal, harga = fetchdata(data)
                return data, tanggal, harga
        except ValueError:
            return None
    else:
        return None

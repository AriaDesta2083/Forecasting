# https://ariadesta2083-fts.streamlit.app/
import streamlit as st
st.set_page_config(
    page_title="SKRIPSI",
    page_icon="images/unej.png",
)

# Judul halaman
a1,a2= st.columns([3,1])
a1.title('TUGAS AKHIR UNIVERSITAS JEMBER ')
a2.image('images/unej.png')

# Informasi personal
st.header('Informasi Mahasiswa')
b1,b2= st.columns([0.1,0.9])
b1.markdown('**Nama**')
b2.markdown(': Aria Desta Prabu')
b1.markdown('**NIM**')
b2.markdown(': 192410102083')
b1.markdown('**Prodi**')
b2.markdown(': Teknologi Informasi')
b1.markdown('**Fakultas**')
b2.markdown(': Fakultas Ilmu Komputer')

# Informasi Skripsi
st.header('Informasi Skripsi')
st.markdown('**Judul :** Implementasi Fuzzy Time Series Cheng Untuk Peramalan Harga Gula Pasir Lokal Di Pasar Tradisional Berbasis Website')
st.markdown('**Dosen Pembimbing 1 :** Prof. Dr. Saiful Bukhori, ST., M.Kom')
st.markdown('**Dosen Pembimbing 2 :** Gayatri Dwi Santika, S.Si., M.Kom')
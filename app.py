import streamlit as st
st.set_page_config(
    page_title="skripsi",
    page_icon="👋",
)

# Judul halaman
st.title('Skripsi')

# Informasi personal
st.header('Informasi Mahasiswa')
st.markdown('**Nama :** Aria Desta Prabu')
st.markdown('**Prodi :** Teknologi Informasi')
st.markdown('**Fakultas :** Fakultas Ilmu Komputer')

# Informasi Skripsi
st.header('Informasi Skripsi')
st.markdown('**Judul :** Implementasi Fuzzy Time Series Cheng Untuk Peramalan Harga Gula Pasir Lokal Di Pasar Tradisional Berbasis Website')
st.markdown('**Dosen Pembimbing 1 :** Prof. Dr. Saiful Bukhori, ST., M.Kom')
st.markdown('**Dosen Pembimbing 2 :** Gayatri Dwi Santika, S.Si., M.Kom')

st.session_state.boolean = True

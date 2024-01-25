import streamlit as st
import pandas as pd
from FTSCheng import flrgroup,bobot

st.set_page_config(page_title="FLRG", page_icon="images/unej.png")
st.header('Fuzzy Logic Relationships Group')

dictFLRG = {
    "CurrentState":list(flrgroup.keys()) , "NextState":list(flrgroup.values()) ,'W':bobot[0],'W*':bobot[1]
}
df = pd.DataFrame(dictFLRG).set_index("CurrentState")
st.dataframe(df,width=10000,height=300,use_container_width=True)
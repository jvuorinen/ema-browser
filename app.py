import streamlit as st

import utils as ut


# App start


st.title("EMA Browzer 🙃")

with st.sidebar:
    st.header("Download dataset for editing")

    file_data = ut.read_xls_file()
    st.download_button(
        label='Download EMA data', 
        data=file_data, 
        file_name='ema_data.xlsx', 
        key='download_button')

    st.header("Upload updated dataset")

    uploaded_file = st.file_uploader("", type="xlsx")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        ut.save_xls_file(bytes_data)

    data = ut.read_data_from_xls()

    st.header("Choose processes to show")

    processes = st.multiselect("", data.keys())

chosen = {}
for p in processes:
    chosen[p] = st.select_slider(p, data[p]["dates"])

if chosen:
    table = ut.get_table(data, chosen).reset_index()
    styled = table.style.background_gradient(
        axis=0, 
        cmap=ut.get_color_map("#F8FBCD", "#D6FAFF", "#FCD3F6"), 
        gmap = table["process"].astype('category').cat.codes
    )
    st.dataframe(styled, hide_index=True)

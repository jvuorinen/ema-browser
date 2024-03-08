import streamlit as st

import utils as ut


# App start


st.title("EMA MAA Timetables")

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

def update_rolling_date(rolling_date: str, date: list[str]):
    for d in date:
        if d > rolling_date:
            return d
    return rolling_date

rolling_date = "1900-01-01"
chosen = {}
for p in processes:
    dates = data[p]["dates"]
    rolling_date = update_rolling_date(rolling_date, dates)
    chosen[p] = st.selectbox(p, dates, index=dates.index(rolling_date))

    # Update rolling date
    ix = dates.index(chosen[p])
    rolling_date = data[p]["data"][ix][-1]

if chosen:
    table = ut.get_table(data, chosen).reset_index()
    styled = table.style.background_gradient(
        axis=0, 
        cmap=ut.get_color_map("#C0EDFF", "#FFC0ED", "#EDFFC0"), 
        gmap = table["process"].astype('category').cat.codes
    )
    st.dataframe(styled, hide_index=True, height=1000)

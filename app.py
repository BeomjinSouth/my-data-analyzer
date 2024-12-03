import streamlit as st
import pandas as pd
from utils.data_processing import create_frequency_table, create_stem_and_leaf
from utils.visualization import plot_histogram

st.title("Excel 데이터 분석 도구")
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "csv"])

if uploaded_file:
    data = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    st.write("데이터 미리보기:")
    st.write(data.head())

    column_name = st.selectbox("분석할 컬럼 선택", data.columns)

    if st.button("도수분포표 생성"):
        freq_table = create_frequency_table(data, column_name)
        st.write(freq_table)

    if st.button("줄기와 잎 그림 생성"):
        stem_leaf = create_stem_and_leaf(data, column_name)
        st.write(stem_leaf)

    if st.button("히스토그램 생성"):
        plt = plot_histogram(data, column_name)
        st.pyplot(plt)

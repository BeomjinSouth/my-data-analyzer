import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np
from utils.data_processing import create_frequency_table, create_stem_and_leaf
from utils.visualization import plot_histogram
import matplotlib.pyplot as plt

# OpenAI API 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI"]["OPENAI_API_KEY"])

st.title("Excel 데이터 분석 도구")

# 세션 상태 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바에 파일 업로더 배치
with st.sidebar:
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            # 데이터 로드
            if uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)
            else:
                data = pd.read_csv(uploaded_file)
            
            # 데이터 기본 정보 표시
            st.write("### 데이터 기본 정보")
            st.write(f"행 수: {data.shape[0]}")
            st.write(f"열 수: {data.shape[1]}")
            
            # 수치형 컬럼만 필터링
            numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_columns:
                st.error("수치형 데이터가 없습니다.")
            
            # 분석할 컬럼 선택
            column_name = st.selectbox("분석할 컬럼 선택", numeric_columns)
        except Exception as e:
            st.error(f"파일 로드 중 오류가 발생했습니다: {str(e)}")

# 메인 영역
if uploaded_file and 'data' in locals() and column_name:
    # 데이터 미리보기
    st.write("### 데이터 미리보기")
    st.dataframe(data.head())
    
    # 기본 통계량
    st.write("### 기본 통계량")
    st.dataframe(data[column_name].describe())
    
    # 분석 도구들을 컬럼으로 배치
    col1, col2 = st.columns(2)
    
    with col1:
        # 도수분포표
        if st.button("도수분포표 생성"):
            st.write("### 도수분포표")
            freq_table = create_frequency_table(data, column_name)
            if isinstance(freq_table, str) and freq_table.startswith("Error"):
                st.error(freq_table)
            else:
                st.dataframe(freq_table)
        
        # 줄기와 잎 그림
        if st.button("줄기와 잎 그림 생성"):
            st.write("### 줄기와 잎 그림")
            stem_leaf = create_stem_and_leaf(data, column_name)
            if isinstance(stem_leaf, str) and stem_leaf.startswith("Error"):
                st.error(stem_leaf)
            else:
                st.text(stem_leaf)
    
    with col2:
        # 히스토그램
        if st.button("히스토그램 생성"):
            st.write("### 히스토그램")
            fig = plot_histogram(data, column_name)
            if isinstance(fig, str) and fig.startswith("Error"):
                st.error(fig)
            else:
                st.pyplot(fig)
        
        # 분석 요약
        if st.button("분석 요약 생성"):
            summary_stats = data[column_name].describe().to_dict()
            summary_prompt = f"""다음은 '{column_name}' 컬럼의 데이터 요약 정보입니다:
            
            {summary_stats}
            
            이 데이터의 특징과 분포에 대해 전문가의 관점에서 분석해주세요."""
            
            st.session_state.messages.append({"role": "user", "content": summary_prompt})
            
            try:
                # OpenAI API를 사용하여 응답 생성
                with st.spinner('분석 요약을 생성하고 있습니다...'):
                    response = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[{"role": m["role"], "content": m["content"]} 
                                for m in st.session_state.messages],
                        temperature=0.7,
                    )
                    
                    # 응답 표시
                    st.write("### AI 분석 요약")
                    st.write(response.choices[0].message.content)
                    
                    # 응답 저장
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response.choices[0].message.content
                    })
            except Exception as e:
                st.error(f"AI 분석 요약 생성 중 오류가 발생했습니다: {str(e)}")

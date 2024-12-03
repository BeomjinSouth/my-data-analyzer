import streamlit as st
from openai import OpenAI  # 새로운 코드 사용 방식
import pandas as pd
from utils.data_processing import create_frequency_table, create_stem_and_leaf
from utils.visualization import plot_histogram

# OpenAI API 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI"]["OPENAI_API_KEY"])

st.title("Excel 데이터 분석 도구")

# 세션 상태 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"  # 새로운 모델 사용
if "messages" not in st.session_state:
    st.session_state.messages = []

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "csv"])

if uploaded_file:
    # 데이터 로드
    data = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    st.write("데이터 미리보기:")
    st.write(data.head())

    # 분석할 컬럼 선택
    column_name = st.selectbox("분석할 컬럼 선택", data.columns)

    # 도수분포표 생성
    if st.button("도수분포표 생성"):
        freq_table = create_frequency_table(data, column_name)
        st.write(freq_table)

    # 줄기와 잎 그림 생성
    if st.button("줄기와 잎 그림 생성"):
        stem_leaf = create_stem_and_leaf(data, column_name)
        st.write(stem_leaf)

    # 히스토그램 생성
    if st.button("히스토그램 생성"):
        plt = plot_histogram(data, column_name)
        st.pyplot(plt)

    # 분석 요약 생성
    if st.button("분석 요약 생성"):
        # 데이터 요약 정보 생성
        summary_stats = data[column_name].describe().to_dict()
        summary_prompt = f"다음은 '{column_name}' 컬럼의 데이터 요약 정보입니다:\n{summary_stats}\n이 데이터를 바탕으로 간단한 분석 요약을 작성해 주세요."

        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": summary_prompt})
        with st.chat_message("user"):
            st.markdown(summary_prompt)

        # OpenAI API를 사용하여 응답 생성
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = ""
            for message in stream:
                content = message.get("choices", [{}])[0].get("delta", {}).get("content", "")
                response += content
                st.markdown(content)

        # 어시스턴트의 응답을 세션 상태에 추가
        st.session_state.messages.append({"role": "assistant", "content": response})


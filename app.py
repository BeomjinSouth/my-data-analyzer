import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# OpenAI API 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI"]["OPENAI_API_KEY"])

st.title("대화형 데이터 분석 도구")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = None

def create_frequency_table(data, column_name, bin_size=10):
    """도수분포표 생성"""
    min_val = data[column_name].min()
    max_val = data[column_name].max()
    bins = np.arange(min_val, max_val + bin_size, bin_size)
    freq_table = pd.cut(data[column_name], bins=bins).value_counts().sort_index()
    freq_df = pd.DataFrame({
        '계급': freq_table.index.astype(str),
        '도수': freq_table.values
    })
    return freq_df

def create_stem_and_leaf(data, column_name, stem_digit=10):
    """줄기와 잎 그림 생성"""
    values = sorted(data[column_name].values)
    stem_leaf = {}
    
    for value in values:
        stem = int(value) // stem_digit
        leaf = int(value) % stem_digit
        if stem not in stem_leaf:
            stem_leaf[stem] = []
        stem_leaf[stem].append(leaf)
    
    # 결과를 보기 좋게 포맷팅
    result = []
    for stem in sorted(stem_leaf.keys()):
        leaves = sorted(stem_leaf[stem])
        result.append(f"{stem:2d} | {' '.join(str(leaf) for leaf in leaves)}")
    
    return '\n'.join(result)

def analyze_request(request, data):
    """사용자 요청 분석 및 처리"""
    try:
        # GPT에게 요청 분석을 의뢰
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """
                당신은 데이터 분석 요청을 해석하는 전문가입니다. 
                사용자의 요청을 분석하여 다음 정보를 JSON 형식으로 반환하세요:
                {
                    "type": "frequency_table" 또는 "stem_leaf",
                    "column": "분석할 컬럼명",
                    "params": {
                        "bin_size": 도수분포표의 계급 크기(frequency_table인 경우),
                        "stem_digit": 줄기의 기준이 되는 숫자(stem_leaf인 경우)
                    }
                }
                """},
                {"role": "user", "content": f"다음 데이터 분석 요청을 해석해주세요. 컬럼 목록: {list(data.columns)}\n요청: {request}"}
            ],
            temperature=0
        )
        
        # GPT의 응답을 파싱
        import json
        analysis_params = json.loads(response.choices[0].message.content)
        
        # 분석 수행
        if analysis_params["type"] == "frequency_table":
            result = create_frequency_table(
                data, 
                analysis_params["column"], 
                analysis_params["params"]["bin_size"]
            )
            st.write("### 도수분포표")
            st.dataframe(result)
            
        elif analysis_params["type"] == "stem_leaf":
            result = create_stem_and_leaf(
                data, 
                analysis_params["column"],
                analysis_params["params"]["stem_digit"]
            )
            st.write("### 줄기와 잎 그림")
            st.text(result)
            
        return True
        
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        return False

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "csv"])
if uploaded_file:
    try:
        # 데이터 로드
        if uploaded_file.name.endswith('.xlsx'):
            st.session_state.data = pd.read_excel(uploaded_file)
        else:
            st.session_state.data = pd.read_csv(uploaded_file)
            
        # 데이터 미리보기
        st.write("### 데이터 미리보기")
        st.dataframe(st.session_state.data.head())
        
    except Exception as e:
        st.error(f"파일 로드 중 오류가 발생했습니다: {str(e)}")

# 채팅 인터페이스
if st.session_state.data is not None:
    st.write("### 분석 요청하기")
    st.write("예시 요청:")
    st.write("- '출산율에 대한 줄기와 잎 그림을 그려줘. 줄기는 십의 자리로 해줘'")
    st.write("- '계급은 출산율, 도수는 도시의 수로 도수분포표를 만들어줘. 계급의 크기는 10으로 해줘'")
    
    # 사용자 입력
    user_input = st.text_input("분석 요청을 입력하세요")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        analyze_request(user_input, st.session_state.data)

# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

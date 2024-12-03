import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_histogram(data, column_name, bins=10):
    """히스토그램 그리기"""
    # 수치형 데이터 확인
    if not np.issubdtype(data[column_name].dtype, np.number):
        return "Error: 수치형 데이터만 히스토그램을 만들 수 있습니다."
    
    # 결측치 제거
    data_clean = data[column_name].dropna()
    
    # 스타일 설정
    plt.style.use('seaborn')
    
    # 새로운 figure 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 히스토그램 그리기
    sns.histplot(data=data_clean, bins=bins, kde=True, ax=ax)
    
    # 그래프 꾸미기
    plt.xlabel(column_name)
    plt.ylabel("빈도수")
    plt.title(f"{column_name}의 분포")
    
    # 그리드 추가
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

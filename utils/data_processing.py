import pandas as pd
import numpy as np

def create_frequency_table(data, column_name, bins=10):
    """도수분포표 생성"""
    # 수치형 데이터 확인
    if not np.issubdtype(data[column_name].dtype, np.number):
        return "Error: 수치형 데이터만 도수분포표를 만들 수 있습니다."
    
    # 결측치 제거
    data_clean = data[column_name].dropna()
    
    # 구간 경계 계산
    min_val = data_clean.min()
    max_val = data_clean.max()
    bin_edges = np.linspace(min_val, max_val, bins + 1)
    
    # 도수분포표 생성
    freq_table = pd.cut(data_clean, bins=bin_edges, include_lowest=True)
    freq_df = pd.DataFrame({
        '구간': freq_table.value_counts().index.astype(str),
        '도수': freq_table.value_counts().values,
        '상대도수': freq_table.value_counts(normalize=True).values,
        '누적도수': freq_table.value_counts().cumsum().values
    }).sort_index()
    
    return freq_df

def create_stem_and_leaf(data, column_name):
    """줄기와 잎 그림 생성"""
    # 수치형 데이터 확인
    if not np.issubdtype(data[column_name].dtype, np.number):
        return "Error: 수치형 데이터만 줄기와 잎 그림을 만들 수 있습니다."
    
    # 결측치 제거
    data_clean = data[column_name].dropna()
    
    # 데이터 정규화 (소수점 처리)
    multiplier = 1
    while any(x % 1 != 0 for x in data_clean):
        data_clean *= 10
        multiplier *= 10
    
    data_sorted = sorted(data_clean)
    stem_leaf = {}
    
    for num in data_sorted:
        num = int(num)
        stem, leaf = divmod(num, 10)
        if stem not in stem_leaf:
            stem_leaf[stem] = []
        stem_leaf[stem].append(leaf)
    
    # 결과를 보기 좋게 포맷팅
    result = []
    for stem in sorted(stem_leaf.keys()):
        leaves = sorted(stem_leaf[stem])
        result.append(f"{stem:2d} | {' '.join(str(leaf) for leaf in leaves)}")
    
    if multiplier > 1:
        result.append(f"\n참고: 원본 데이터에 {multiplier}를 곱한 결과입니다.")
    
    return '\n'.join(result)

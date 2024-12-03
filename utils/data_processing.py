import pandas as pd

def create_frequency_table(data, column_name, bins=10):
    """도수분포표 생성"""
    freq_table = pd.cut(data[column_name], bins=bins).value_counts().sort_index()
    return freq_table

def create_stem_and_leaf(data, column_name):
    """줄기와 잎 그림 생성"""
    data_sorted = sorted(data[column_name])
    stem_leaf = {}
    for num in data_sorted:
        stem, leaf = divmod(num, 10)
        stem_leaf.setdefault(stem, []).append(leaf)
    return stem_leaf

import matplotlib.pyplot as plt

def plot_histogram(data, column_name, bins=10):
    """히스토그램 그리기"""
    plt.figure(figsize=(8, 6))
    plt.hist(data[column_name], bins=bins, edgecolor="black")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram")
    plt.tight_layout()
    return plt

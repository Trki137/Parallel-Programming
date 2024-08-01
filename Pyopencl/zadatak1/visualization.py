import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_results(csv_file):
    df = pd.read_csv(csv_file)

    pivot_table = df.pivot_table(values="Time (s)", index="L", columns="G")

    plt.figure(figsize=(10, 8))
    plt.title("Execution Time for Different Combinations of G and L")
    c = plt.pcolor(pivot_table, cmap='viridis')
    plt.colorbar(c, label='Time (s)')

    plt.xlabel('G (Global Work Size)')
    plt.ylabel('L (Local Work Size)')

    plt.xticks(np.arange(0.5, len(pivot_table.columns), 1), pivot_table.columns, rotation=90)
    plt.yticks(np.arange(0.5, len(pivot_table.index), 1), pivot_table.index)

    plt.savefig("heatmap")
    plt.show()

    plt.figure(figsize=(10, 8))
    for L in pivot_table.index:
        plt.plot(pivot_table.columns, pivot_table.loc[L], marker='o', label=f'L={L}')

    plt.title("Execution Time vs Global Work Size for Different Local Work Sizes")
    plt.xlabel('G (Global Work Size)')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True)
    plt.savefig("line plot")
    plt.show()


if __name__ == "__main__":
    plot_results('results.csv')

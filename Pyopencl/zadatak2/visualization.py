import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import dataframe_image as dfi

if __name__ == '__main__':
    data = pd.read_csv('results.csv')

    sequential_time = data.loc[0, 'Time (s)']
    data = data.drop(0)

    data['Speedup'] = sequential_time / data['Time (s)']
    dfi.export(data, "results_with_speedup.png")

    plt.figure(figsize=(14, 8))
    sns.lineplot(x='M', y='Speedup', hue='L', data=data, marker='o')
    plt.xscale('log', base=2)
    plt.xlabel('Global Size (G)')
    plt.ylabel('Speedup')
    plt.title('Speedup vs Global Size for Different Local Sizes')
    plt.legend(title='Local Size (L)')
    plt.savefig("speedup")
    plt.show()

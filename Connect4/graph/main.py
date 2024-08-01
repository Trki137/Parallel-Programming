import numpy as np
import pandas as pd
from pandas.plotting import table
from matplotlib import pyplot as plt


def create_tables():
    data = pd.read_csv('../results.csv')
    task_depths = data['Task Depth'].unique()

    for task_depth in task_depths:
        filtered_data = data[data['Task Depth'] == task_depth][['P', 'Execution Time (seconds)', 'Depth']]
        filtered_data['Execution Time (seconds)'] = filtered_data['Execution Time (seconds)'].round(6)
        pivot_table = filtered_data.pivot(index='Depth', columns='P', values='Execution Time (seconds)')
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('tight')
        ax.axis('off')
        table(ax, pivot_table, loc='center', cellLoc='center')
        ax.set_title(f'Execution Time vs Number of Processors for Task Depth {task_depth}', fontsize=14, pad=12)
        plt.savefig(f'table_task_depth_{task_depth}.png', bbox_inches='tight')


def create_speedup_graph():
    data = pd.read_csv('../results.csv')
    data_list_of_dicts = data.to_dict(orient='records')

    plt.figure(figsize=(10, 6))

    p1_times = [entry['Execution Time (seconds)'] for entry in data_list_of_dicts if entry['P'] == 1]
    base_exec_time = sum(p1_times) / len(p1_times)

    for i in range(1, 4):
        filtered = list(filter(lambda x: x['Task Depth'] == i, data_list_of_dicts))
        x = []
        y = []
        for j in range(6, -1, -1):
            entry = filtered[j]
            exec_time = entry['Execution Time (seconds)']
            p = entry['P']
            speed_up = base_exec_time / exec_time
            x.append(p)
            y.append(speed_up)

        plt.plot(x, y, marker='o', linestyle='-', label=f'Task Depth: {i}')

    max_processors = max(data['P'])
    ideal_x = list(range(1, max_processors + 1))
    ideal_y = ideal_x
    plt.plot(ideal_x, ideal_y, linestyle='--', color='gray', label='Ideal Speed-Up')

    plt.xlabel('Broj procesora (P)')
    plt.ylabel('Ubrzanje')
    plt.title('Ubrzanje s brojem procesora za različite dubine zadataka')
    plt.legend()
    plt.savefig("Ubrzanje.png")
    plt.show()


def create_efficiency_graph():
    data = pd.read_csv('../results.csv')
    data_list_of_dicts = data.to_dict(orient='records')

    plt.figure(figsize=(10, 6))

    for i in range(1, 4):
        filtered = list(filter(lambda x: x['Task Depth'] == i, data_list_of_dicts))
        base_exec_time = filtered[7]['Execution Time (seconds)']
        x = []
        y = []
        for j in range(7, -1, -1):
            entry = filtered[j]
            exec_time = entry['Execution Time (seconds)']
            p = entry['P']
            eff = base_exec_time / (exec_time * p)
            x.append(p)
            y.append(eff)

        plt.plot(x, y, marker='o', linestyle='-', label=f'Task Depth: {i}')

    plt.xlabel('Broj procesora (P)')
    plt.ylabel('Učinkovitost')
    plt.title('Učinkovitost s obzirom na broj procesora za različite dubine zadataka')
    plt.legend()
    plt.savefig("Ucinkovitost.png")
    plt.show()


if __name__ == '__main__':
    create_tables()
    create_speedup_graph()
    create_efficiency_graph()

import csv
from pathlib import Path


def csv_results(filepath: str, csv_data):
    file_exists = Path(filepath).exists()

    with open(filepath, 'a', newline='') as file:
        headers = ['N', 'Time (s)', 'L', 'M']
        writer = csv.DictWriter(file, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        data = {
            'N': csv_data['N'],
            'Time (s)': csv_data['time'],
            'L': csv_data['L'],
            'M': csv_data['M']
        }

        writer.writerow(data)


def csv_results_task_3(filepath: str, csv_data):
    file_exists = Path(filepath).exists()

    with open(filepath, 'a', newline='') as file:
        headers = ['Error', 'Time (s)', 'Iter time (s)']
        writer = csv.DictWriter(file, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        data = {
            'Error': csv_data['error'],
            'Time (s)': csv_data['time'],
            'Iter time (s)': csv_data['one_iter_time'],
        }

        writer.writerow(data)

import csv
import codecs
import pandas as pd


def convert_csv(path):
    raw_data = list(csv.reader(codecs.open(
        path, 'rU', 'utf-16'), delimiter="\t", quotechar='"'))

    row = 0
    vars = []
    filtered_data = []
    data = []

    while raw_data[row][0] != 'Nsig':
        row += 1
    else:
        n_var = int(raw_data[row][1])
        row += 1

    for _ in range(n_var):
        vars.append(raw_data[row][1])
        row += 1
    else:
        filtered_data.append(vars)

    while raw_data[row][0] != 'StartOfData':
        row += 1
    else:
        row += 1

    while row < len(raw_data):
        data = list(map(float, raw_data[row]))
        filtered_data.append(data)
        row += 1

    with open(path + "_filtered.csv", "w+", newline='', encoding='utf-16') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerows(filtered_data)


def read_as_array(path):
    raw_data = list(csv.reader(codecs.open(
        path, 'rU', 'utf-16'), delimiter="\t", quotechar='"'))

    row = 0
    vars = []
    filtered_data = []
    data = []

    while raw_data[row][0] != 'Nsig':
        row += 1
    else:
        n_var = int(raw_data[row][1])
        row += 1

    for _ in range(n_var):
        vars.append(raw_data[row][1])
        row += 1
    else:
        filtered_data.append(vars)

    while raw_data[row][0] != 'StartOfData':
        row += 1
    else:
        row += 1

    while row < len(raw_data):
        data = list(map(float, raw_data[row]))
        filtered_data.append(data)
        row += 1

    return filtered_data


def write_csv(array, path):
    with open(path, "w+", newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerows(array)


def read_df(path):
    convert_csv(path)
    df = pd.read_csv(path+"_filtered.csv", encoding='utf-16')
    return df


if __file__ == '__main__':

    file_paths = [
        'data\Cable PVC 5C\Cable PVC 5C DATA',
        'data\Cable PVC 10C\Cable PVC 10C DATA',
        'data\Cable PVC 15C\Cable PVC 15C DATA',
        'data\Cable PVC 20C\Cable PVC 20C DATA',
        'data\Cable PVC 25C\Cable PVC 25C DATA'
    ]

    for p in file_paths:
        convert_csv(p)

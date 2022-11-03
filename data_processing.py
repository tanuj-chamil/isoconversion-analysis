import pandas as pd
from read_data import read_df


def remove_error_data(data, col):
    threshold = 0.1
    previous = data[col].iloc[0]
    data = data.reset_index()
    error_points = []
    for index, row in data.iterrows():
        if previous < row[col] or abs(row[col]-previous) > threshold:
            error_points.append(index)
        else:
            previous = row[col]
    return data.drop(index=error_points)


if __name__ == "__main__":
    file_path = 'data\Cable PVC 5C\Cable PVC 5C DATA'
    data = read_df(file_path)
    remove_error_data(data, 2)

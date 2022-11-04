import pandas as pd
from read_data import read_df
import plotly as pt


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


def remove_dehydration(data, col):
    data = data.copy()

    plateaus = []
    threshold_height = 0.075
    threshold_width = 150
    epsilon = 25

    start = 0
    end = 0
    data = data.reset_index()

    for index, row in data.iterrows():
        if abs(data[col].iloc[start]-row[col]) < threshold_height:
            end = index
        else:
            if end-start > threshold_width:
                plateaus.append((start, end))
            start = end

    _plateaus = []
    for i in range(len(plateaus)-1):
        if abs(plateaus[i][1] - plateaus[i+1][0]) == 0:
            _plateaus.append((plateaus[i][0], plateaus[i+1][1]))
        else:
            _plateaus.append(plateaus[i])

    def merge(plateaus):
        p = []
        count = 0
        for i in range(len(plateaus)-1):
            if plateaus[i][1] >= plateaus[i+1][0]:
                count += 1
                p.append((plateaus[i][0], plateaus[i+1][1]))
            else:
                p.append(plateaus[i])

        if count == 2:
            return plateaus
        else:
            return merge(p)

    p = merge(_plateaus)

    return [(data['Temperature (°C)'].iloc[i[0]], data['Temperature (°C)'].iloc[i[1]]) for i in p]


if __name__ == "__main__":
    file_path = 'data\Cable PVC 5C\Cable PVC 5C DATA'
    data = read_df(file_path)
    remove_error_data(data, 2)

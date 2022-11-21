from read_data import read_df
import numpy as np
from scipy.signal import savgol_filter
from scipy.constants import R
import statsmodels.api as sm
lowess = sm.nonparametric.lowess


def remove_error_data(data, col):
    threshold = 0.1
    previous = data[col].iloc[0]
    data = data.reset_index()
    error_points = []
    for index, row in data.iterrows():
        if previous < row[col] or abs(row[col]-previous) > threshold:
            data.at[index, col] = previous
        else:
            previous = row[col]
    return data


def step_f(val, threshold):
    if abs(val) <= threshold:
        return 1
    return 0


def nearest(df, col, val):
    return df.iloc[(df[col] - val).abs().argsort()[0], :]


def find_plateau(data, threshold=0.0001, custom=[]):
    data['MA'] = data['Weight (mg)'].rolling(window=25).mean()
    data['dMA'] = data['MA'].diff()
    def f(x): return step_f(x, threshold)
    data['P'] = data['dMA'].apply(f)

    intervals = []
    i = []
    for index, row in data.iterrows():
        if row['P'] == 1:
            i.append(index)
        else:
            if i != []:
                intervals.append(
                    (data.iloc[i[0], 1], data.iloc[i[-1], 1]))
            i = []
    return [nearest(data, 'Temperature (°C)', (i[0]+i[1])/2)['Weight (mg)'] for i in intervals] if custom == [] else custom


def get_reaction(data, m_o, m_f):
    reaction = data[data['Weight (mg)'] >= m_f]
    reaction = reaction[reaction['Weight (mg)'] <= m_o]
    return reaction


def conversion(data):
    m_o = data['Weight (mg)'].iloc[0]
    m_f = data['Weight (mg)'].iloc[data.shape[0]-1]
    def alpha(m): return (m_o-m)/(m_o-m_f)
    data['alpha'] = data['Weight (mg)'].apply(alpha)
    return data


def differentiate(data):
    def d(index):
        return (data['alpha'].iloc[index+1]-data['alpha'].iloc[index]) / (data['T'].iloc[index+1]-data['T'].iloc[index])

    d_alpha = []
    for index in range(data.shape[0]):
        if index == 0:
            dadt = d(index)
        elif index == data.shape[0]-1:
            dadt = d(index-1)
        else:
            dadt = (d(index-1)+d(index))/2
        d_alpha.append(dadt)

    data['d_alpha'] = d_alpha
    return data


def differentiate_T(data):
    def d(index):
        return (data['T'].iloc[index+1]-data['T'].iloc[index]) / (data['Temperature (°C)'].iloc[index+1]-data['Temperature (°C)'].iloc[index])

    dT = []
    for index in range(data.shape[0]):
        if index == 0:
            dTdt = d(index)
        elif index == data.shape[0]-1:
            dTdt = d(index-1)
        else:
            dTdt = (d(index-1)+d(index))/2
        dT.append(dTdt)

    data['dT'] = dT
    return data


def smooth(data):
    data['s_da'] = lowess(data['d_alpha'],
                          data['T'], frac=0.02, return_sorted=False)
    return data


def smooth_E(data):
    data['s_Ea'] = lowess(data['Ea (kJ/mol)'],
                          data['alpha'], frac=0.02, return_sorted=False)
    return data


def fit(data, beta):
    data['y'] = beta*data['s_da'].apply(np.log)
    data['x'] = -(1/R)*data['T'].apply(lambda t: 1/(t+273.15))
    return data


if __name__ == "__main__":
    file_path = 'data\Cable PVC 5C\Cable PVC 5C DATA'
    data = read_df(file_path)
    remove_error_data(data, 2)

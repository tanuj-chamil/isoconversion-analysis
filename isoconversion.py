from scipy.interpolate import interp1d, splrep, CubicSpline
from data_processing import *
from read_data import read_df
import pandas as pd
from scipy import stats

pd.options.plotting.backend = "plotly"


def get_curves(file):
    data = read_df(file)[['Temperature (°C)', 'Weight (mg)']]

    data['T'] = 273.15 + data['Temperature (°C)']

    data = remove_error_data(data, 'Weight (mg)')

    m = find_plateau(data, threshold=0.0004)[:2]

    data = get_reaction(data, m[0], m[1])

    data = conversion(data)

    data = differentiate(data)

    data = smooth(data)

    data = data.sort_values('alpha')

    data = data.drop_duplicates(subset=['alpha'])

    data.plot(x='T', y='alpha')

    CURVE_T = CubicSpline(y=data['T'],
                          x=data['alpha'],
                          bc_type='natural')

    CURVE_DADT = CubicSpline(y=data['d_alpha'],
                             x=data['alpha'],
                             bc_type='natural')

    return (CURVE_DADT, CURVE_T)


def get_all_curves(beta):
    file_paths = [
        'data\Cable PVC {0}C\Cable PVC {0}C DATA'.format(b) for b in beta]
    curves = []
    for f in file_paths:
        curves.append(get_curves(f))
    return curves


def calc_parameters(alpha, betas, curves):
    y = [np.log(betas[i]*curves[i][0](alpha)) for i in range(4)]
    x = [(-1/(R*curves[i][1](alpha))) for i in range(4)]
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    paras = (alpha, slope, intercept, r ** 2)
    return paras

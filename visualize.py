from data_processing import remove_error_data
from read_data import read_as_array as read
import pandas as pd
from read_data import read_df
from data_processing import *
from visualize import *
pd.options.plotting.backend = "plotly"


def plot(data, r=[], x_data='T', y_data='Weight (mg)'):
    p = data.plot(x=x_data, y=y_data, kind='line')
    for i in r:
        p.add_hline(y=i, line_width=1, line_color="green")
        #p.add_hline(x=i[1], line_width=1, line_color="red")
    return p

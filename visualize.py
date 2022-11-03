import pandas as pd
from read_data import read_as_array as read
from data_processing import remove_error_data

file_path = 'data\Cable PVC 5C\Cable PVC 5C DATA'
raw_data = read(file_path)

data = remove_error_data(raw_data, 2)

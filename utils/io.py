import pandas as pd


def read_enbw_dataset(filepath):
    def str2float(x):
        return float(x.replace(',', '.'))

    data = pd.read_csv(filepath, delimiter=';', converters={'value': str2float})
    data['timestampLocal'] = pd.to_datetime(data.timestampLocal)

    return data
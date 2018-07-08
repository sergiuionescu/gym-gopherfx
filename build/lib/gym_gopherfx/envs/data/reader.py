import os
import pandas as pd


class Reader(object):
    @staticmethod
    def read(source='rates/'):
        df = []
        for rates_file in sorted(os.listdir(source)):
            key, ext = os.path.splitext(rates_file)
            df.append({'name': key, 'rates': pd.read_csv(
                source + rates_file, names=['date', 'rate'])})
        return df

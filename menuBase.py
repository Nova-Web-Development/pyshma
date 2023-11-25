import pandas as pd


class DataMenu:
    def __init__(self):
        self.data = pd.read_excel('МЕНЮ ОБЩЕЕ НЕБО.XLSX').iloc[1:, 1:]

    def getAllDatas(self):
        dt1 = self.data.iloc[:11, :].rename(
            columns={'понедельник 09.10': 'Основные блюда', 'Unnamed: 2': 'g', 'Unnamed: 3': 'rub'})

        dt2 = self.data.iloc[self.data[self.data['понедельник 09.10'] == 'Основные блюда'].index[0]:20, :].rename(
            columns={'понедельник 09.10': 'Основные блюда', 'Unnamed: 2': 'g', 'Unnamed: 3': 'rub'})

        dt3 = self.data.iloc[self.data[self.data['понедельник 09.10'] == 'Гарниры'].index[0]:28, :].rename(
            columns={'понедельник 09.10': 'Гарниры', 'Unnamed: 2': 'g', 'Unnamed: 3': 'rub'})

        dt4 = self.data.iloc[self.data[self.data['понедельник 09.10'] == 'завтрак'].index[0]:46, :].rename(
            columns={'понедельник 09.10': 'завтрак', 'Unnamed: 2': 'g', 'Unnamed: 3': 'rub'})

        dt5 = self.data.iloc[self.data[self.data['понедельник 09.10'] == 'выпечка'].index[0]:, :].rename(
            columns={'понедельник 09.10': 'выпечка', 'Unnamed: 2': 'g', 'Unnamed: 3': 'rub'})

        return [dt1, dt2, dt3, dt4, dt5]

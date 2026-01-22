import pandas as pd


class Meta:
    def __init__(self, df):
        self._df = df
        self._hydrophobicity_platforms=[]
        self._hydrophobicity_platforms.append('SMAC')
        self._hydrophobicity_platforms.append('HIC')

    def calculate(self):
        abs=self._df['Name'].unique()
        out=[]
        for ab in abs:
            h_df = self._df[(self._df['Name'] == ab) & (self._df['Platform'].isin(self._hydrophobicity_platforms))]
            c_df = self._df[(self._df['Name'] == ab) & (~self._df['Platform'].isin(self._hydrophobicity_platforms))]
            h = h_df['Rank'].mean()
            c = c_df['Rank'].mean()
            m = ((h**2) + (c**2))**0.5
            #m = (h+c)/2
            out.append([ab, m, c, h])
        out = pd.DataFrame(out, columns=['Name', 'Meta', 'Hydrophobicity', 'Charge'])
        return out



import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
PATH = PATH.joinpath('Dataset')
df = pd.read_excel(PATH.joinpath('ICC Test Bat 3001.xlsx'))

for i in range(len(df['HS'])):
    if '*' in str(df['HS'][i]):
        df['HS'][i] = df['HS'][i].rstrip('*')

to_delete = df[df['Runs'] == '-'].index
df.drop(to_delete, inplace=True)
cleaned_data = df.drop(['Span', 'Player Profile'], axis=1)

df_copy = cleaned_data.copy()
df_copy.set_index('Player', inplace=True, drop=True)
print(df_copy.to_string())
var = 'Avg'
df_copy = df_copy[var]
#print(df_copy)
# my_dict = df_copy.to_dict('records')
# print(my_dict)

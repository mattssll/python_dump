import pandas as pd

df = pd.read_json('data_from_api.json', lines = True)
print(df.columns)
print(df['Category'].value_counts())
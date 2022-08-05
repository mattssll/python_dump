from datetime import datetime
import pandas as pd
from io import BytesIO
from google.cloud import storage
import os

bucket = 'rfm-vectux-customers'
read_path = 'gs://lake_tests/dummie.csv'
batch_timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
write_path = 'gs://lake_tests/test_ml'
write_final_csv = 'gs://lake_tests/test_ml/final_predictions'
i = 0
chunksize = 5000
df = pd.read_csv(read_path, chunksize = chunksize, iterator = True)

header = True
file_names = []
for chunk in df:
    print(f"i: {i}, chunksize: {chunksize}")
    i += 1
    file_name = f"{write_path}/{i}_{batch_timestamp}_pred.csv"
    file_names.append(file_name)
    chunk.to_csv(file_name, header=header, index=False)
    header = False  # only put header in first file

file_names_str = ' '.join(file_names)
shell_command_join_csvs = f'gsutil compose {file_names_str} {write_final_csv}/finalpred_{batch_timestamp}.csv'

print("execute shell command now:")
os.system(shell_command_join_csvs)

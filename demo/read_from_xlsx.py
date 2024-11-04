import pandas as pd


file_path = './test.xlsx'

# 读取 Excel 文件
df = pd.read_excel(
    file_path,
    sheet_name=0,
    header=0,
    engine='openpyxl')

for index, row in df.iterrows():
    print(index, row['编号'])

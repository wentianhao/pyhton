import pandas as pd
import numpy as np

from openpyxl import load_workbook

a = np.random.randn(365,4)
writer = pd.ExcelWriter('data.xlsx',engine='openpyxl')
print(writer)
book = load_workbook('data.xlsx')
writer.book = book
df = pd.DataFrame(a)
df.to_excel(writer,sheet_name='test1')
writer.save()
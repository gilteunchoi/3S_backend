from django.test import TestCase
import pandas as pd

# Create your tests here.
df1 = pd.read_excel('sss_com/first.xls', header=None)
# print(df1)
print(len(df1))
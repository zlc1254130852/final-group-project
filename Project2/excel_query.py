import pandas as pd

df = pd.read_excel("static/object_detection_label_return_value.xlsx")

def excel_find(index):
    value = df.iloc[2+index,1]
    print(value)
    return value
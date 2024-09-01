import pandas as pd

def get_column_names(file_path):
    df = pd.read_csv(file_path)
    return df.columns.tolist(), df

import pandas as pd
df = pd.read_csv("insurance.csv")
def get_min_max(df, title) -> tuple[float, float]:
    return df[title].min(), df[title].max()




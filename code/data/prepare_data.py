import pandas as pd

df = pd.read_csv("data/london_noise.csv")

df = df.dropna(subset=["lat", "lon", "laeq"])

df = df[
    (df["lat"].between(51.2, 51.8)) &
    (df["lon"].between(-0.6, 0.3)) 
]

df.to_json("data/london_noise.json", orient="records")
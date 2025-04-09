import pandas as pd

df = pd.read_csv("C:\\Users\\laure\\PycharmProjects\\Data-Driven Anomaly Detection\\data\\dataset_30min.csv")

#checken of er data in zit
print(df.head())

#beschrijvende data bekijken
print(df.columns)
print(df.info())

print(df.describe())

print("null waarden")
print(df.isnull().sum())

print(df["event.category"].unique())

print(df["data_stream.dataset"].unique())
print(df["session.iflow_bytes"].unique())


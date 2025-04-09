import pandas as pd

df = pd.read_csv("C:\\Users\\laure\\PycharmProjects\\Data-Driven Anomaly Detection\\data\\Untitled_discover_search.csv")

#checken of er data in zit
print(df.head())

#beschrijvende data bekijken
print(df.columns)
print(df.info())

print(df.describe())




print("null waarden")
print(df.isnull().sum())




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Zorg ervoor dat je CSV-bestand al is ingelezen
# Bijvoorbeeld:
# df = pd.read_csv("../data/untitled_discover_search.csv")

# Als de timestamp-kolom nog niet als datetime is geconverteerd:
df["@timestamp"] = pd.to_datetime(df["@timestamp"], format="%b %d, %Y @ %H:%M:%S.%f")


# --- 1. Bar chart: Frequentie van event.action ---
plt.figure(figsize=(10, 6))
action_counts = df["event.action"].value_counts()
sns.barplot(x=action_counts.index, y=action_counts.values, palette="viridis")
plt.title("Frequentie van event.action")
plt.xlabel("Event Action")
plt.ylabel("Aantal")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- 2. Histogram: Distributie van een numerieke kolom (bijvoorbeeld 'protocol') ---
plt.figure(figsize=(8, 5))
plt.hist(df["protocol"], bins=20, color="skyblue", edgecolor="black")
plt.title("Verdeling van protocol")
plt.xlabel("Protocol")
plt.ylabel("Frequentie")
plt.show()

# --- 3. Tijdreeks: Aantal logs per minuut ---
# Eerst zetten we de timestamp als index
df_time = df.set_index("@timestamp")
# Resample per minuut en tel het aantal logs
logs_per_minute = df_time.resample("T").size()

plt.figure(figsize=(12, 6))
logs_per_minute.plot()
plt.title("Aantal logs per minuut")
plt.xlabel("Tijd")
plt.ylabel("Aantal logs")
plt.tight_layout()
plt.show()

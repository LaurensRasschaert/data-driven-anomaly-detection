from elasticsearch import Elasticsearch
import pandas as pd

# Maak verbinding met je Elasticsearch-cluster
es = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    # Voeg eventueel credentials toe als dat nodig is:
    # http_auth=('Laurens', 'A,knS%q8M{H2/YR$]_)Z;4+KcxzWp')
)

# Vervang 'jouw_index_naam' door de daadwerkelijke naam van je index
index_name = "jouw_index_naam"

# Bouw een query op om alle documenten op te halen, maar beperk het aantal tot 2000
query = {
    "query": {
        "match_all": {}
    },
    "size": 2000
}

# Voer de query uit
response = es.search(index=index_name, body=query)

# Haal de documenten (hits) uit de response
hits = response["hits"]["hits"]

# Zet de _source data van elk document om in een lijst
records = [hit["_source"] for hit in hits]

# Laad de data in een Pandas DataFrame
df = pd.DataFrame(records)

# Bekijk de eerste paar regels
print(df.head())

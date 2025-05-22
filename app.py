import pandas as pd
import requests
from sqlalchemy import create_engine

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
         return response.json()


    else:
        print(f"failed to retrieve data {response.status_code}")
        return None
def get_all_pokemon(limit=200):
    url = f"{base_url}pokemon?limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data=response.json()
        return [p["name"] for p in data["results"]]
    else:
        print(f"failed to retrieve data {response.status_code}")
        return None
pokemon_list = get_all_pokemon(limit=200)
all_data = []

for name in pokemon_list:
    info = get_pokemon_info(name)
    if info:
        types = [t['type']['name'] for t in info['types']]
        data = {
            "name" : info['name'],
            "types": info["types"],
            "height": info["height"],
            "weight": info["weight"],
            "id": info["id"],
            "base_experience": info["base_experience"]
        }
        all_data.append(data)

df = pd.DataFrame(all_data)
df.to_csv("pokemon_data.csv", index=False)
print(" Saved all results to pokemon_data.csv")



# Load CSV
df = pd.read_csv("pokemon_data.csv")

# Connect to MySQL (change username, password, db name)
user = 'pokemon_user'
password = 'password123'
host = 'localhost'  # or your DB endpoint
database = 'pokemon'

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Upload to MySQL
df.to_sql('pokemon', con=engine, if_exists='replace', index=False)
print("Uploaded to MySQL")






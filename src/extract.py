import os
from dotenv import load_dotenv
import pandas as pd
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

load_dotenv()

api_secopii = os.getenv("API_SECOPII")
csv_file = 'data/raw/secop2_data_2024-2025.csv'
file_exists = os.path.exists(csv_file)

def extract_data() -> pd.DataFrame:
    global file_exists

    limit=50000
    df = pd.read_csv(csv_file) if file_exists else pd.DataFrame()
    offset = len(df)
        
  
    while True:
        try:
            response = requests.get(api_secopii, 
                                    params={'$where': 'fecha_de_firma >= "2024-01-01" AND fecha_de_firma < "2026-01-01"',
                                            '$order': 'fecha_de_firma ASC',
                                            '$limit': limit, 
                                            '$offset': offset,
                                            }, timeout=(60,120))
            if response.status_code == 200:
                data = response.json()
                if not data:
                    print("No more data to fetch.")
                    break
           
                offset += limit

                df = pd.DataFrame(data)

                df.to_csv(csv_file, mode='a', header=not file_exists, index=False)

                if not file_exists:
                    file_exists = True

                print(f"Fetched {len(data)} records...")

            elif response.status_code == 503:
                print("Service unavailable. Retrying...")
                continue

            elif response.status_code == 429:
                print("Rate limit exceeded. Retrying...")
                continue

            else:
                print(f"Error: {response.status_code}")
                break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"Request failed: {e}")
            break
    
    

    df = pd.read_csv(csv_file) if file_exists else pd.DataFrame()
    print(f"Csv file with {len(df)} records...")

    return df
    
if __name__ == "__main__":
    df = extract_data()
    print(f"Total registros: {len(df)}")
    print(df.head())
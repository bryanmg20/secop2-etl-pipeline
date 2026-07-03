import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    # crea la conexion a PostgreSQL
    url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(url)

def load(tables):
    engine = get_engine()
    
    # orden importante: primero las que no tienen FK
    tables['location'].to_sql('location', engine, if_exists='replace', index=False)
    tables['date'].to_sql('dim_date', engine, if_exists='replace', index=False)
    tables['provider'].to_sql('provider', engine, if_exists='replace', index=False)
    tables['entity'].to_sql('entity', engine, if_exists='replace', index=False)
    tables['contract'].to_sql('contract', engine, if_exists='replace', index=False)
    
    print("Data uploaded successfully to PostgreSQL database.")
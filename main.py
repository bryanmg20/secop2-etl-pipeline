from src.extract import extract_data
from src.transform import transform_data
from src.load import load

def main():
    print("starting pipeline...")
    
    df = extract_data()
    print("extraction completed")
    
    table = transform_data(df)
    print("Transformation completed")
    
    load(table)
    print("Pipeline finished successfully")

if __name__ == "__main__":
    main()
from src.extract import extract_data
from src.transform import transform_data
from src.load import load
from src.logger import get_logger

logger = get_logger(__name__)

def main() -> None:
    """Main function to orchestrate the ETL pipeline."""
    try:
        logger.info("Starting extraction...")
        df = extract_data()
        logger.info("Extraction completed")
        
        logger.info("Starting transformation...")
        table = transform_data(df)
        logger.info("Transformation completed")
        
        logger.info("Starting loading...")
        load(table)
        logger.info("Pipeline finished successfully")
    
    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
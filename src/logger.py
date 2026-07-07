import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                "logs/pipeline.log",
                maxBytes=5*1024*1024,
                backupCount=3
            ),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(name)
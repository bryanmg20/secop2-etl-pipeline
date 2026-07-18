from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import db_conn
import logging
from pydantic import BaseModel
from datetime import date

logger = logging.getLogger(__name__)

from .routes.rankings import app as ranking_router
from .routes.contract import app as contract_router
from .routes.actors import app as actors_router

app = FastAPI()

app.include_router(ranking_router, prefix="/contracts", tags=["Rankings"])
app.include_router(contract_router, prefix="/contracts", tags=["Contracts"])
app.include_router(actors_router, tags=["Actors"])

class StatsResponse(BaseModel):
    total_contracts: int
    total_entities: int
    total_providers: int
    total_departments: int
    total_cities: int
    latest_signing_date: date
    database_size: str

class HealthResponse(BaseModel):
    status: str

class root_response(BaseModel):
    message: str

@app.get("/", response_model=root_response)
async def root():
    return root_response(message="Welcome to the SECOP2 Electronic Contracts API! if you want to see the documentation go to /docs or /redoc")

@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(db_conn.get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    if result == 1:
        return HealthResponse(status="healthy")
    elif result is None:
        return HealthResponse(status="unhealthy")

@app.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(db_conn.get_db)):
    query = """
    SELECT 
        (SELECT COUNT(c.id_contract) FROM secop2ce.contract c) AS total_contracts,
        (SELECT MAX(d.date) FROM secop2ce.contract c INNER JOIN secop2ce.dim_date d ON c.id_signing_date = d.id_date) AS latest_signing_date,
        (SELECT COUNT(e.id_entity) FROM secop2ce.entity e) AS total_entities,
        (SELECT COUNT(p.id_provider) FROM secop2ce.provider p) AS total_providers,
        (SELECT COUNT(DISTINCT d.department) FROM secop2ce.location d WHERE department != 'NO DEFINIDO') AS total_departments,
        (SELECT COUNT(d.city) FROM secop2ce.location d WHERE city != 'NO DEFINIDO') AS total_cities,
        pg_size_pretty(pg_database_size(current_database())) AS db_size
    """

    try:
        result = db.execute(text(query))
        stats = result.fetchone()

        if stats is None:
            logger.error("No statistics found in the database")
            raise HTTPException(status_code=404, detail="Statistics not found")
    

        return StatsResponse(
            total_contracts= stats.total_contracts,
            total_entities= stats.total_entities,
            total_providers= stats.total_providers,
            total_departments= stats.total_departments,
            total_cities= stats.total_cities,
            latest_signing_date= stats.latest_signing_date,
            database_size= stats.db_size
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics from the database")
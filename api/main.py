from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import db_conn
import logging
from .schemas import ErrorResponse
from .models import HealthResponse, StatsResponse, root_response
from .queries.stats import STATS_QUERY

logger = logging.getLogger(__name__)

from .routes.rankings import app as ranking_router
from .routes.contract import app as contract_router
from .routes.actors import app as actors_router

app = FastAPI(
    title="SECOP II Electronics Contracts API",
    version="0.1.0",
    description=(
        "API to query public contracts, entities, providers, and rankings derived "
        "from the SECOP II dataset."
    ),
    contact={"name": "Bryan", "email": "bryanmontoyagalindo@outlook.com"},
)

app.include_router(ranking_router, prefix="/contracts", tags=["Rankings"])
app.include_router(contract_router, prefix="/contracts", tags=["Contracts"])
app.include_router(actors_router, tags=["Actors"])

@app.get(
    "/",
    response_model=root_response,
    summary="API overview",
    description="Returns a welcome message with the interactive documentation route.",
)
async def root():
    return root_response(message="Welcome to the SECOP2 Electronic Contracts API! if you want to see the documentation go to /docs or /redoc")

@app.get(
    "/health",
    response_model=HealthResponse,
    responses={200: {"model": HealthResponse, "description": "API and database are healthy"}, 500: {"model": ErrorResponse, "description": "Database dependency failed"}},
    summary="Health check",
    description="Checks that the API and database are responding correctly.",
)
async def health_check(db: Session = Depends(db_conn.get_db)):

    try:
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return HealthResponse(status="healthy")
        else:
            logger.error("Health check failed: unexpected database response")
            raise HTTPException(status_code=500, detail="Database dependency failed")
    except Exception as e:
        logger.error(f"Error in /health: {e}")
        raise HTTPException(status_code=500, detail="Error occurred while checking health")


@app.get(
    "/stats",
    response_model=StatsResponse,
    responses={200: {"model": StatsResponse, "description": "Estadísticas generales de la base de datos"}, 404: {"model": ErrorResponse, "description": "No statistics were found"}, 500: {"model": ErrorResponse, "description": "Unexpected error while querying statistics"}},
    summary="General statistics",
    description="Returns general metrics about the contracts catalog loaded in the database.",
)
async def get_stats(db: Session = Depends(db_conn.get_db)):
    try:
        result = db.execute(text(STATS_QUERY))
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
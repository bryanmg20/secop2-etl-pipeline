from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db_conn import get_db
from sqlalchemy import text
from api.schemas import ErrorResponse
from api.models import ContractsByDepartmentResponse, ContractsByYearResponse, TopEntitiesResponse, TopProvidersResponse
from api.queries.rankings import CONTRACTS_BY_DEPARTMENT_QUERY, CONTRACTS_BY_YEAR_QUERY, TOP_ENTITIES_QUERY, TOP_PROVIDERS_QUERY
import logging

logger = logging.getLogger(__name__)

app = APIRouter()
#top-providers
@app.get(
    "/top-providers",
    response_model=list[TopProvidersResponse],
    responses={200: {"model": list[TopProvidersResponse], "description": "Top providers", "content": {"application/json": {"example": [{"id_provider": 713062461, "document_provider": "8.786.444", "name_provider": "ABELARDO DE LA ESPRIELLA PEREZ", "contract_count": 2}]}}}, 500: {"model": ErrorResponse, "description": "Error while retrieving top providers"}},
    summary="Top providers",
    description="Returns the providers with the highest number of contracts in the database.",
)
async def get_top_providers(db: Session = Depends(get_db)):
    try:
        result = db.execute(text(TOP_PROVIDERS_QUERY))
        top_providers = result.fetchall()

        return [
            TopProvidersResponse(
                id_provider=provider[0],
                document_provider=provider[1],
                name_provider=provider[2],
                contract_count=provider[3]
            )
            for provider in top_providers
        ]

    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error in /top-providers: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving top providers")
#top-entities
@app.get(
    "/top-entities",
    response_model=list[TopEntitiesResponse],
    responses={200: {"model": list[TopEntitiesResponse], "description": "Top entities"}, 500: {"model": ErrorResponse, "description": "Error while retrieving top entities"}},
    summary="Top entities",
    description="Returns the entities with the highest number of contracts in the database.",
)
async def get_top_entities(db: Session = Depends(get_db)):
    try:
        result = db.execute(text(TOP_ENTITIES_QUERY))
        top_entities = result.fetchall()

        return [
            TopEntitiesResponse(
                id_entity=entity[0],
                nit_entity=entity[1],
                name_entity=entity[2],
                contract_count=entity[3]
            )
            for entity in top_entities
        ]

    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error in /top-entities: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving top entities")

@app.get(
    "/by-department",
    response_model=list[ContractsByDepartmentResponse],
    responses={200: {"model": list[ContractsByDepartmentResponse], "description": "Contracts grouped by department"}, 500: {"model": ErrorResponse, "description": "Error while retrieving contracts by department"}},
    summary="Contracts by department",
    description="Groups contracts by department and returns aggregated value metrics.",
)
async def get_contracts_by_department(db: Session = Depends(get_db)):
    try:
        result = db.execute(text(CONTRACTS_BY_DEPARTMENT_QUERY))
        contracts_by_department = result.fetchall()

        return [
            ContractsByDepartmentResponse(
                department=department[0],
                contract_count=department[1],
                total_contract_value=department[2],
                avg_value=department[3],
                biggest_contract_value=department[4]
            )
            for department in contracts_by_department
        ]

    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error in /by-department: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving contracts by department")

@app.get(
    "/by-year",
    response_model=list[ContractsByYearResponse],
    responses={200: {"model": list[ContractsByYearResponse], "description": "Contracts grouped by year"}, 500: {"model": ErrorResponse, "description": "Error while retrieving contracts by year"}},
    summary="Contracts by year",
    description="Groups contracts by signing year and returns aggregated value metrics.",
)
async def get_contracts_by_year(db: Session = Depends(get_db)):
    try:
        result = db.execute(text(CONTRACTS_BY_YEAR_QUERY))
        contracts_by_year = result.fetchall()

        return [
            ContractsByYearResponse(
                year=year[0],
                contract_count=year[1],
                total_contract_value=year[2],
                avg_value=year[3],
                biggest_contract_value=year[4]
            )
            for year in contracts_by_year
        ]

    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error in /by-year: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving contracts by year")
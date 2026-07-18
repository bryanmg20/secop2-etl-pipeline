from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db_conn import get_db
from sqlalchemy import text
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

app = APIRouter()


class TopProvidersResponse(BaseModel):
    id_provider: int
    document_provider: str
    name_provider: str
    contract_count: int


#top-providers
@app.get("/top-providers", response_model = list[TopProvidersResponse])
async def get_top_providers(db: Session = Depends(get_db)):

    query = """
    SELECT p.id_provider,p.provider_document,p.name_provider, COUNT(c.id_contract) AS contract_count
    FROM secop2ce.provider p
    INNER JOIN secop2ce.contract c ON p.id_provider = c.id_provider
    GROUP BY p.id_provider, p.name_provider
    ORDER BY contract_count DESC
    LIMIT 100
    """
    try:
        result = db.execute(text(query))
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
        logger.error(f"Error en /top-providers: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving top providers")


class TopEntitiesResponse(BaseModel):
    id_entity: int
    nit_entity: int
    name_entity: str
    contract_count: int

#top-entities
@app.get("/top-entities", response_model = list[TopEntitiesResponse])
async def get_top_entities(db: Session = Depends(get_db)):
    query = """
    SELECT e.id_entity,e.nit_entity,e.name_entity, COUNT(c.id_contract) AS contract_count
    FROM secop2ce.entity e
    INNER JOIN secop2ce.contract c ON e.id_entity = c.id_entity
    GROUP BY e.id_entity
    ORDER BY contract_count DESC
    LIMIT 100
    """
    try:
        result = db.execute(text(query))
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
        logger.error(f"Error en /top-entities: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving top entities")

#by-department
class ContractsByDepartmentResponse(BaseModel):
    department: str
    contract_count: int
    total_contract_value: float
    avg_value: float
    biggest_contract_value: float

@app.get("/by-department", response_model = list[ContractsByDepartmentResponse])
async def get_contracts_by_department(db: Session = Depends(get_db)):
    query = """
    SELECT d.department, COUNT(c.id_contract) AS contract_count, SUM(c.contract_value) AS total_contract_value,
           AVG(c.contract_value) AS avg_value, MAX(c.contract_value) AS biggest_contract_value
    FROM secop2ce.location d
    INNER JOIN secop2ce.entity e ON d.id_location = e.id_location
    INNER JOIN secop2ce.contract c ON e.id_entity = c.id_entity
    WHERE d.department != 'NO DEFINIDO'
    GROUP BY d.department
    ORDER BY contract_count DESC
    """
    try:
        result = db.execute(text(query))
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
        logger.error(f"Error en /by-department: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving contracts by department")

#by-year
class ContractsByYearResponse(BaseModel):
    year: int
    contract_count: int
    total_contract_value: float
    avg_value: float
    biggest_contract_value: float

@app.get("/by-year", response_model = list[ContractsByYearResponse])
async def get_contracts_by_year(db: Session = Depends(get_db)):
    query = """
    SELECT d.year, COUNT(c.id_contract) AS contract_count, SUM(c.contract_value) AS total_contract_value,
           AVG(c.contract_value) AS avg_value, MAX(c.contract_value) AS biggest_contract_value
    FROM secop2ce.dim_date d
    INNER JOIN secop2ce.contract c ON d.id_date = c.id_signing_date
    GROUP BY d.year
    ORDER BY d.year DESC
    """
    try:
        result = db.execute(text(query))
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
        logger.error(f"Error en /by-year: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving contracts by year")
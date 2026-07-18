from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db_conn import get_db
from sqlalchemy import text
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

app = APIRouter()


#serch-entity
class EntitySearchResponse(BaseModel):
    id_entity: int
    nit_entity: int
    name_entity: str 
    order_entity: str | None
    sector_entity: str | None
    branch_entity: str | None
    centralized_entity: bool | None

@app.get("/search/entity", response_model=list[EntitySearchResponse])
async def search_entity(q: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            e.id_entity,
            e.nit_entity,
            e.name_entity,
            e.order_entity,
            e.sector_entity,
            e.branch_entity,
            e.centralized_entity
        FROM secop2ce.entity AS e
        WHERE 
            e.name_entity ILIKE :search_query OR
            CAST(e.nit_entity AS TEXT) ILIKE :search_query
        ORDER BY e.name_entity
        LIMIT 10
    """)
    search_query = f"%{q}%"
    try:
        results = db.execute(query, {"search_query": search_query}).fetchall()
        return [EntitySearchResponse(**row._mapping) for row in results]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error searching for entities: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

#search-provider
class ProviderSearchResponse(BaseModel):
    id_provider: int
    type_of_provider: str | None
    provider_document: str | None
    name_provider: str | None
    is_pyme: bool | None
    is_group: bool | None

@app.get("/search/provider", response_model=list[ProviderSearchResponse])
async def search_provider(q: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            p.id_provider,
            p.type_of_provider,
            p.provider_document,
            p.name_provider,
            p.is_pyme,
            p.is_group
        FROM secop2ce.provider AS p
        WHERE 
            p.name_provider ILIKE :search_query OR
            CAST(p.provider_document AS TEXT) ILIKE :search_query
        ORDER BY p.name_provider
        LIMIT 10
    """)
    search_query = f"%{q}%"
    try:
        results = db.execute(query, {"search_query": search_query}).fetchall()
        return [ProviderSearchResponse(**row._mapping) for row in results]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error searching for providers: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")











#info-entity
class ContracttypeDistribution(BaseModel):
    contract_type: str
    total_contracts: int
    total_value_contracted: float | None

class EntityResponse(BaseModel):
    id_entity: int
    nit_entity: int
    name_entity: str 
    order_entity: str | None
    sector_entity: str | None
    branch_entity: str | None
    centralized_entity: bool | None

    total_contracts: int 
    total_value_paid: float | None
    total_value_contracted: float | None
    id_contract_most_value: str | None
    document_provider_most_contracts: str | None
    year_most_contracts: int | None
    contract_type_distribution: list[ContracttypeDistribution] | None

@app.get("/entity/{id_entity}", response_model=EntityResponse)
async def get_entity(id_entity: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            e.id_entity,
            e.nit_entity,
            e.name_entity,
            e.order_entity,
            e.sector_entity,
            e.branch_entity,
            e.centralized_entity,
            COUNT(c.id_contract) AS total_contracts,
            SUM(c.paid_value) AS total_value_paid,
            SUM(c.contract_value) AS total_value_contracted,
            (SELECT c2.id_contract FROM secop2ce.contract AS c2 WHERE c2.id_entity = e.id_entity ORDER BY c2.contract_value DESC LIMIT 1) AS id_contract_most_value,
            (SELECT p.provider_document FROM secop2ce.provider AS p INNER JOIN secop2ce.contract AS c3 ON p.id_provider = c3.id_provider WHERE c3.id_entity = e.id_entity GROUP BY p.provider_document ORDER BY COUNT(c3.id_contract) DESC LIMIT 1) AS document_provider_most_contracts,
            (SELECT EXTRACT(YEAR FROM d.date) FROM secop2ce.contract AS c4 INNER JOIN secop2ce.dim_date d ON c4.id_signing_date = d.id_date WHERE c4.id_entity = e.id_entity GROUP BY EXTRACT(YEAR FROM d.date) ORDER BY COUNT(c4.id_contract) DESC LIMIT 1) AS year_most_contracts
        
        FROM secop2ce.entity AS e
        LEFT JOIN secop2ce.contract c ON e.id_entity = c.id_entity
        WHERE e.id_entity = :id_entity
        GROUP BY e.id_entity
    """)

    try:
        result = db.execute(query, {"id_entity": id_entity}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        # Fetch contract type distribution
        contract_type_query = text("""
            SELECT 
                c.contract_type,
                COUNT(c.id_contract) AS total_contracts,
                SUM(c.contract_value) AS total_value_contracted
            FROM 
                secop2ce.contract c
            WHERE 
                c.id_entity = :id_entity
            GROUP BY 
                c.contract_type
        """)

        contract_type_result = db.execute(contract_type_query, {"id_entity": id_entity}).fetchall()
        contract_type_distribution = [ContracttypeDistribution(**row._mapping) for row in contract_type_result]

        return EntityResponse(**result._mapping, contract_type_distribution=contract_type_distribution)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching entity data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


class ProviderResponse(BaseModel):
    id_provider: int
    type_of_provider: str | None
    provider_document: str | None
    name_provider: str | None
    is_pyme: bool | None
    is_group: bool | None

    total_contracts: int 
    total_value_paid: float | None
    total_value_contracted: float | None
    id_contract_most_value: str | None
    nit_entity_most_contracts: int | None
    year_most_contracts: int | None
    contract_type_distribution: list[ContracttypeDistribution] | None


#provider-info
@app.get("/provider/{id_provider}", response_model=ProviderResponse)
async def get_provider(id_provider: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            p.id_provider,
            p.type_of_provider,
            p.provider_document,
            p.name_provider,
            p.is_pyme,
            p.is_group,
            COUNT(c.id_contract) AS total_contracts,
            SUM(c.paid_value) AS total_value_paid,
            SUM(c.contract_value) AS total_value_contracted,
            (SELECT c2.id_contract FROM secop2ce.contract AS c2 WHERE c2.id_provider = p.id_provider ORDER BY c2.contract_value DESC LIMIT 1) AS id_contract_most_value,
            (SELECT e.nit_entity FROM secop2ce.entity AS e INNER JOIN secop2ce.contract AS c3 ON e.id_entity = c3.id_entity WHERE c3.id_provider = p.id_provider GROUP BY e.nit_entity ORDER BY COUNT(c3.id_contract) DESC LIMIT 1) AS nit_entity_most_contracts,
            (SELECT EXTRACT(YEAR FROM d.date) FROM secop2ce.contract AS c4 INNER JOIN secop2ce.dim_date d ON c4.id_signing_date = d.id_date WHERE c4.id_provider = p.id_provider GROUP BY EXTRACT(YEAR FROM d.date) ORDER BY COUNT(c4.id_contract) DESC LIMIT 1) AS year_most_contracts
        
        FROM secop2ce.provider AS p
        LEFT JOIN secop2ce.contract c ON p.id_provider = c.id_provider
        WHERE p.id_provider = :id_provider
        GROUP BY p.id_provider
    """)

    try:
        result = db.execute(query, {"id_provider": id_provider}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Fetch contract type distribution
        contract_type_query = text("""
            SELECT 
                c.contract_type,
                COUNT(c.id_contract) AS total_contracts,
                SUM(c.contract_value) AS total_value_contracted
            FROM 
                secop2ce.contract c
            WHERE 
                c.id_provider = :id_provider
            GROUP BY 
                c.contract_type
        """)

        contract_type_result = db.execute(contract_type_query, {"id_provider": id_provider}).fetchall()
        contract_type_distribution = [ContracttypeDistribution(**row._mapping) for row in contract_type_result]

        return ProviderResponse(**result._mapping, contract_type_distribution=contract_type_distribution)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching provider data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

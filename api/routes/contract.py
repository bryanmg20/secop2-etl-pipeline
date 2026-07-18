from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db_conn import get_db
from sqlalchemy import text
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

app = APIRouter()

#limit-offset pagination
class PaginationParams(BaseModel):
    limit: int = Field(default=100, ge=1, le=5000)
    offset: int = Field(default=0, ge=0)

class ContractResponse(BaseModel):
    id_contract: str
    id_entity: int
    id_provider: int

    #Dates
    id_contract_start_date: int | None
    id_contract_end_date: int | None
    id_signing_date: int | None
    id_liquidation_start_date: int | None
    id_liquidation_end_date: int | None
    id_last_update_date: int | None

    #Contract information
    contract_state: str | None
    method_of_contracting: str | None
    source_of_resources: str | None
    destination_of_expense: str | None
    contract_type: str | None

    #Monetary values
    contract_value: float | None
    paid_value: float | None
    advance_payment_value: float | None
    pending_payment_value: float | None
    invoiced_value: float | None
    amortized_value: float | None
    pending_amortization_value: float | None
    pending_execution_value: float | None

    #Duration
    additional_days: int | None
    contract_can_be_extended: bool | None

    #Booleans
    liquidation: bool | None
    environmental_obligation: bool | None
    is_post_conflict: bool | None
    allows_advance_payment: bool | None
    post_consumer_obligations: bool | None
    reversion: bool | None

@app.get("/", response_model=list[ContractResponse])
async def get_contracts(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):

    
    query = text("""
        SELECT * FROM secop2ce.contract
        LIMIT :limit OFFSET :offset
    """)
    try:
        result = db.execute(query, {"limit": pagination.limit, "offset": pagination.offset}).fetchall()
        return [ContractResponse(**row._mapping) for row in result]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching contracts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@app.get("/search", response_model=list[ContractResponse])
async def search_contracts(q: str, pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    sql_query = text("""
        SELECT * FROM secop2ce.contract
        WHERE 
            id_contract ILIKE :query
            OR COALESCE(contract_state, '') ILIKE :query
            OR COALESCE(method_of_contracting, '') ILIKE :query
            OR COALESCE(source_of_resources, '') ILIKE :query
            OR COALESCE(destination_of_expense, '') ILIKE :query
            OR COALESCE(contract_type, '') ILIKE :query
        LIMIT :limit OFFSET :offset
    """)
    try:
        result = db.execute(sql_query, {"query": f"%{q}%", "limit": pagination.limit, "offset": pagination.offset}).fetchall()
        return [ContractResponse(**row._mapping) for row in result]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error searching contracts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




#filer
class ContractFilterParams(BaseModel):
    contract_state: str | None = None
    method_of_contracting: str | None = None
    source_of_resources: str | None = None
    destination_of_expense: str | None = None
    contract_type: str | None = None
    year: int | None = None
    department: str | None = None
    min_contract_value: float | None = None
    max_contract_value: float | None = None

@app.get("/filter", response_model=list[ContractResponse])
async def filter_contracts(filters: ContractFilterParams = Depends(), pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    
    joins = []
    conditions = ["1=1"]
    params = {}

    # Agrega el JOIN solo si necesita filtrar por año
    if filters.year:
        joins.append("INNER JOIN secop2ce.dim_date d ON c.id_signing_date = d.id_date")
        conditions.append("d.year = :year")
        params["year"] = filters.year

    # Agrega los dos JOINs solo si necesita filtrar por departamento
    if filters.department:
        joins.append("INNER JOIN secop2ce.entity e ON c.id_entity = e.id_entity")
        joins.append("INNER JOIN secop2ce.location l ON e.id_location = l.id_location")
        conditions.append("l.department = :department")
        params["department"] = filters.department.upper()

    # Filtros directos de la tabla contract — sin JOIN
    if filters.contract_state:
        conditions.append("c.contract_state = :contract_state")
        params["contract_state"] = filters.contract_state.upper()
    if filters.contract_type:
        conditions.append("c.contract_type = :contract_type")
        params["contract_type"] = filters.contract_type.upper()
    if filters.method_of_contracting:
        conditions.append("c.method_of_contracting = :method_of_contracting")
        params["method_of_contracting"] = filters.method_of_contracting.upper()
    if filters.source_of_resources:
        conditions.append("c.source_of_resources = :source_of_resources")
        params["source_of_resources"] = filters.source_of_resources.upper()
    if filters.destination_of_expense:
        conditions.append("c.destination_of_expense = :destination_of_expense")
        params["destination_of_expense"] = filters.destination_of_expense.upper()
    if filters.min_contract_value is not None:
        conditions.append("c.contract_value >= :min_contract_value")
        params["min_contract_value"] = filters.min_contract_value
    if filters.max_contract_value is not None:
        conditions.append("c.contract_value <= :max_contract_value")
        params["max_contract_value"] = filters.max_contract_value

    params["limit"] = pagination.limit
    params["offset"] = pagination.offset

    base_query = f"""
        SELECT c.* FROM secop2ce.contract c
        {" ".join(joins)}
        WHERE {" AND ".join(conditions)}
        LIMIT :limit OFFSET :offset
    """

    try:
        result = db.execute(text(base_query), params).fetchall()
        return [ContractResponse(**row._mapping) for row in result]

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error filtering contracts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#by-id
@app.get("/{id_contract}", response_model=ContractResponse)
async def get_contract_by_id(id_contract: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT * FROM secop2ce.contract
        WHERE id_contract = :id_contract
    """)
    try:
        result = db.execute(query, {"id_contract": id_contract}).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Contract not found")
        return ContractResponse(**result._mapping)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching contract by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#contracts-per-entity
@app.get("/entity/{nit_entity}", response_model=list[ContractResponse])
async def get_contracts_per_entity(nit_entity: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT c.* FROM secop2ce.contract AS c
        INNER JOIN secop2ce.entity AS e ON c.id_entity = e.id_entity
        WHERE e.nit_entity = :nit_entity
    """)
    try:
        result = db.execute(query, {"nit_entity": nit_entity}).fetchall()
        return [ContractResponse(**row._mapping) for row in result]

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching contracts per entity: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#contracts-per-provider
@app.get("/provider/{nit_cc_provider}", response_model=list[ContractResponse])
async def get_contracts_per_provider(nit_cc_provider: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT c.* FROM secop2ce.contract AS c
        INNER JOIN secop2ce.provider AS p ON c.id_provider = p.id_provider
        WHERE p.provider_document = :nit_cc_provider 
    """)
    try:
        result = db.execute(query, {"nit_cc_provider": nit_cc_provider}).fetchall()
        return [ContractResponse(**row._mapping) for row in result]

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching contracts per provider: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

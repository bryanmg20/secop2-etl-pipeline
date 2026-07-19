from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.db_conn import get_db
from sqlalchemy import text
from api.schemas import ErrorResponse
from api.models import ContracttypeDistribution, EntityResponse, EntitySearchResponse, ProviderResponse, ProviderSearchResponse
from api.queries.actors import ENTITY_CONTRACT_TYPE_DISTRIBUTION_QUERY, ENTITY_DETAIL_QUERY, ENTITY_SEARCH_QUERY, PROVIDER_CONTRACT_TYPE_DISTRIBUTION_QUERY, PROVIDER_DETAIL_QUERY, PROVIDER_SEARCH_QUERY
import logging

logger = logging.getLogger(__name__)

app = APIRouter()


@app.get(
    "/search/entity",
    response_model=list[EntitySearchResponse],
    responses={200: {"model": list[EntitySearchResponse], "description": "Entities found", "content": {"application/json": {"example": [{"id_entity": 12, "nit_entity": 900123456, "name_entity": "Municipio de Antioquia", "order_entity": "order_example", "sector_entity": "Public", "branch_entity": "Local", "centralized_entity": False}]}}}, 500: {"model": ErrorResponse, "description": "Error while searching entities"}},
    summary="Search entities",
    description="Searches entities by name or NIT using partial matching and returns a summarized result.",
)
async def search_entity(q: str = Query(..., description="Free-text search term for entities.", example="bogota"), db: Session = Depends(get_db)):
    search_query = f"%{q}%"
    try:
        results = db.execute(text(ENTITY_SEARCH_QUERY), {"search_query": search_query}).fetchall()
        return [EntitySearchResponse(**row._mapping) for row in results]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error searching for entities: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.get(
    "/search/provider",
    response_model=list[ProviderSearchResponse],
    responses={200: {"model": list[ProviderSearchResponse], "description": "Providers found", "content": {"application/json": {"example": [{"id_provider": 34, "type_of_provider": "Company", "provider_document": "900000001", "name_provider": "Acme S.A.S.", "is_pyme": True, "is_group": False}]}}}, 500: {"model": ErrorResponse, "description": "Error while searching providers"}},
    summary="Search providers",
    description="Searches providers by name or document using partial matching and returns a summarized result.",
)
async def search_provider(q: str = Query(..., description="Free-text search term for providers.", example="acme"), db: Session = Depends(get_db)):
    search_query = f"%{q}%"
    try:
        results = db.execute(text(PROVIDER_SEARCH_QUERY), {"search_query": search_query}).fetchall()
        return [ProviderSearchResponse(**row._mapping) for row in results]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error searching for providers: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@app.get(
    "/entity/{id_entity}",
    response_model=EntityResponse,
    responses={200: {"model": EntityResponse, "description": "Entity details", "content": {"application/json": {"example": {"id_entity": 12, "nit_entity": 900123456, "name_entity": "Bogota City", "order_entity": "Municipality", "sector_entity": "Public", "branch_entity": "Local", "centralized_entity": False, "total_contracts": 24, "total_value_paid": 150000000.0, "total_value_contracted": 210000000.0, "id_contract_most_value": "CT-4004", "document_provider_most_contracts": "900000001", "year_most_contracts": 2024, "contract_type_distribution": [{"contract_type": "Service provision", "total_contracts": 18, "total_value_contracted": 180000000.0}]}}}}, 404: {"model": ErrorResponse, "description": "Entity not found"}, 500: {"model": ErrorResponse, "description": "Error while retrieving entity details"}},
    summary="Entity details",
    description="Returns aggregated metrics and contract-type distribution for a specific entity.",
)
async def get_entity(id_entity: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(text(ENTITY_DETAIL_QUERY), {"id_entity": id_entity}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        # Fetch contract type distribution
        contract_type_result = db.execute(text(ENTITY_CONTRACT_TYPE_DISTRIBUTION_QUERY), {"id_entity": id_entity}).fetchall()
        contract_type_distribution = [ContracttypeDistribution(**row._mapping) for row in contract_type_result]

        return EntityResponse(**result._mapping, contract_type_distribution=contract_type_distribution)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching entity data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
#provider-info
@app.get(
    "/provider/{id_provider}",
    response_model=ProviderResponse,
    responses={200: {"model": ProviderResponse, "description": "Provider details", "content": {"application/json": {"example": {"id_provider": 34, "type_of_provider": "Company", "provider_document": "900000001", "name_provider": "Acme S.A.S.", "is_pyme": True, "is_group": False, "total_contracts": 11, "total_value_paid": 90000000.0, "total_value_contracted": 120000000.0, "id_contract_most_value": "CT-5005", "nit_entity_most_contracts": 900123456, "year_most_contracts": 2024, "contract_type_distribution": [{"contract_type": "Works", "total_contracts": 7, "total_value_contracted": 95000000.0}]}}}}, 404: {"model": ErrorResponse, "description": "Provider not found"}, 500: {"model": ErrorResponse, "description": "Error while retrieving provider details"}},
    summary="Provider details",
    description="Returns aggregated metrics and contract-type distribution for a specific provider.",
)
async def get_provider(id_provider: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(text(PROVIDER_DETAIL_QUERY), {"id_provider": id_provider}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Fetch contract type distribution
        contract_type_result = db.execute(text(PROVIDER_CONTRACT_TYPE_DISTRIBUTION_QUERY), {"id_provider": id_provider}).fetchall()
        contract_type_distribution = [ContracttypeDistribution(**row._mapping) for row in contract_type_result]

        return ProviderResponse(**result._mapping, contract_type_distribution=contract_type_distribution)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching provider data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

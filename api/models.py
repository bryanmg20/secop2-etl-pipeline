from datetime import date

from pydantic import BaseModel, Field


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


class EntitySearchResponse(BaseModel):
    id_entity: int
    nit_entity: int
    name_entity: str
    order_entity: str | None
    sector_entity: str | None
    branch_entity: str | None
    centralized_entity: bool | None


class ProviderSearchResponse(BaseModel):
    id_provider: int
    type_of_provider: str | None
    provider_document: str | None
    name_provider: str | None
    is_pyme: bool | None
    is_group: bool | None


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


class PaginationParams(BaseModel):
    limit: int = Field(
        default=100,
        ge=1,
        le=5000,
        description="Maximum number of records to return per page.",
        example=100,
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip for pagination.",
        example=0,
    )


class ContractResponse(BaseModel):
    id_contract: str
    id_entity: int
    id_provider: int
    id_contract_start_date: int | None
    id_contract_end_date: int | None
    id_signing_date: int | None
    id_liquidation_start_date: int | None
    id_liquidation_end_date: int | None
    id_last_update_date: int | None
    contract_state: str | None
    method_of_contracting: str | None
    source_of_resources: str | None
    destination_of_expense: str | None
    contract_type: str | None
    contract_value: float | None
    paid_value: float | None
    advance_payment_value: float | None
    pending_payment_value: float | None
    invoiced_value: float | None
    amortized_value: float | None
    pending_amortization_value: float | None
    pending_execution_value: float | None
    additional_days: int | None
    contract_can_be_extended: bool | None
    liquidation: bool | None
    environmental_obligation: bool | None
    is_post_conflict: bool | None
    allows_advance_payment: bool | None
    post_consumer_obligations: bool | None
    reversion: bool | None


class ContractFilterParams(BaseModel):
    contract_state: str | None = Field(default=None, description="Contract status, for example ACTIVO or TERMINADO.", example="ACTIVO")
    method_of_contracting: str | None = Field(default=None, description="Procurement method used.", example="Contratación directa")
    source_of_resources: str | None = Field(default=None, description="Source of the contract resources.", example="SISTEMA DE RENTAS GENERALES")
    destination_of_expense: str | None = Field(default=None, description="Destination of the associated expense.", example="Educación")
    contract_type: str | None = Field(default=None, description="Contract type.", example="Prestación de servicios")
    year: int | None = Field(default=None, description="Year the contract was signed.", example=2024)
    department: str | None = Field(default=None, description="Department of the contracting party, as text or full name.", example="ANTIOQUIA")
    min_contract_value: float | None = Field(default=None, description="Minimum contract value.", example=1000000)
    max_contract_value: float | None = Field(default=None, description="Maximum contract value.", example=50000000)


class TopProvidersResponse(BaseModel):
    id_provider: int = Field(..., description="Id of the provider", example=700306053)
    document_provider: str = Field(..., description="Document of the provider", example="860002400")
    name_provider: str = Field(..., description="Name of the provider", example="LA PREVISORA S.A. COMPANIA DE SEGUROS")
    contract_count: int = Field(..., description="Count of the contracts", example=3759)


class TopEntitiesResponse(BaseModel):
    id_entity: int = Field(..., description="Id of the entity", example=702486788)
    nit_entity: int = Field(..., description="NIT of the entity", example=900959048)
    name_entity: str = Field(..., description="Name of the entity", example="SUBRED INTEGRADA DE SERVICIOS DE SALUD SUR OCCIDENTE ESE")
    contract_count: int = Field(..., description="Count of the contracts", example=63974)


class ContractsByDepartmentResponse(BaseModel):
    department: str = Field(..., description="Department of the contracts", example="DISTRITO CAPITAL DE BOGOTA")
    contract_count: int = Field(..., description="Count of the contracts", example=1792819)
    total_contract_value: float = Field(..., description="Total value of the contracts", example=452429908652600.0)
    avg_value: float = Field(..., description="Average value per contract", example=252356712.34)
    biggest_contract_value: float = Field(..., description="Biggest contract value found", example=4949735040000.0)


class ContractsByYearResponse(BaseModel):
    year: int = Field(..., description="Year of the contracts", example=2024)
    contract_count: int = Field(..., description="Cantidad de contratos", example=320)
    total_contract_value: float = Field(..., description="Valor total contratado", example=2500000000.0)
    avg_value: float = Field(..., description="Average value per contract", example=7812500.0)
    biggest_contract_value: float = Field(..., description="Biggest contract value found", example=750000000.0)
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date

class StreetPointsRequest(BaseModel):
    start_point: List[float]
    end_point: List[float]
    num_points: int

class StreetPointsResponse(BaseModel):
    points: List[List[float]]

class InstallationDetailBase(BaseModel):
    installation_date: date
    contractor_name: Optional[str]

class LightSpecificationBase(BaseModel):
    bulb_type: Optional[str]
    bulb_manufacturer: Optional[str]
    wattage: Optional[int]

class HardwareInformationBase(BaseModel):
    pole_type: Optional[str]
    pole_height: Optional[float]
    control_system_type: Optional[str]

class WarrantyInformationBase(BaseModel):
    component_name: str
    warranty_start: date
    warranty_end: date
    warranty_terms: Optional[str]

class CostAndPricingBase(BaseModel):
    installation_cost: Optional[float]
    bulb_cost: Optional[float]
    fixture_cost: Optional[float]
    electricity_cost: Optional[float]
    maintenance_cost: Optional[float]

class MaintenanceHistoryBase(BaseModel):
    maintenance_date: date
    maintenance_type: Optional[str]
    cost: Optional[float]
    contractor_name: Optional[str]
    notes: Optional[str]

class IssueReportBase(BaseModel):
    issue_date: date
    issue_description: Optional[str]
    resolution_status: Optional[str]
    resolution_date: Optional[date]
    time_to_resolve: Optional[float]

class EnergyConsumptionBase(BaseModel):
    average_daily_consumption: Optional[float]
    average_monthly_consumption: Optional[float]
    operating_hours: Optional[int]

class OperationalStatusBase(BaseModel):
    current_status: Optional[str]
    last_status_update: Optional[date]

class LifeCycleInformationBase(BaseModel):
    component: Optional[str]
    expected_lifespan: Optional[int]
    replacement_schedule: Optional[date]

class StreetLightBase(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str]
    ward: Optional[str]
    street_id: Optional[int]

class StreetLightCreate(StreetLightBase):
    installation_detail: Optional[InstallationDetailBase]
    light_specification: Optional[LightSpecificationBase]
    hardware_information: Optional[HardwareInformationBase]
    warranties: Optional[List[WarrantyInformationBase]]
    cost_pricing: Optional[CostAndPricingBase]
    energy_consumption: Optional[EnergyConsumptionBase]
    operational_status: Optional[OperationalStatusBase]
    life_cycle_information: Optional[LifeCycleInformationBase]

class StreetLightOperationCreate(BaseModel):
    street_light_id: int
    timestamp: date
    power_consumption: float
    voltage_levels: float
    current_fluctuations: float
    temperature: float
    environmental_conditions: str
    current_fluctuations_env: float
    fault_type: int

class StreetLight(StreetLightBase):
    id: int
    installation_detail: Optional[InstallationDetailBase]
    light_specification: Optional[LightSpecificationBase]
    hardware_information: Optional[HardwareInformationBase]
    warranties: Optional[List[WarrantyInformationBase]]
    cost_pricing: Optional[CostAndPricingBase]
    maintenance_histories: Optional[List[MaintenanceHistoryBase]]
    issue_reports: Optional[List[IssueReportBase]]
    energy_consumption: Optional[EnergyConsumptionBase]
    operational_status: Optional[OperationalStatusBase]
    life_cycle_information: Optional[LifeCycleInformationBase]

    class Config:
        from_attributes = True
class Coordinates(BaseModel):
    latitude: float
    longitude: float

class StreetLocation(BaseModel):
    start: Coordinates
    end: Coordinates

class StreetBasicInfo(BaseModel):
    id: int
    street_name: str
    ward: Optional[str]
    total_lights: int
    total_power_consumption: float
    operational_summary: Dict[str, int]
    recent_issues: int
    coordinates: Optional[StreetLocation] = None

    class Config:
        from_attributes = True

class MaintenanceRecord(BaseModel):
    date: date
    type: str
    cost: float

class LightEnergyConsumption(BaseModel):
    light_id: int
    monthly_consumption: float
    daily_consumption: float

class LightInstallation(BaseModel):
    installation_date: date
    contractor_name: Optional[str]

class LightSpecification(BaseModel):
    bulb_type: Optional[str]
    bulb_manufacturer: Optional[str]
    wattage: Optional[int]

class OperationalStatus(BaseModel):
    current_status: str
    last_status_update: Optional[date]

class LightInfo(BaseModel):
    id: int
    location: Coordinates
    address: Optional[str]
    installation: Optional[LightInstallation]
    specifications: Optional[LightSpecification]
    status: Optional[OperationalStatus]

class MaintenanceSummary(BaseModel):
    total_maintenance_records: int
    recent_maintenance: List[MaintenanceRecord]

class EnergySummary(BaseModel):
    total_monthly_consumption: float
    average_daily_consumption: float
    per_light_consumption: List[LightEnergyConsumption]

class CostSummary(BaseModel):
    total_installation_cost: float
    total_maintenance_cost: float
    total_electricity_cost: float
    total_cost: float

class WarrantySummary(BaseModel):
    active_warranties: int
    expiring_soon: int

class StreetInfo(BaseModel):
    street_name: str
    ward: Optional[str]
    description: Optional[str]

class StreetDetailedInfo(BaseModel):
    street_info: StreetInfo
    lights_info: List[LightInfo]
    maintenance_summary: MaintenanceSummary
    energy_summary: EnergySummary
    cost_summary: CostSummary
    warranty_summary: WarrantySummary

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.db import get_db
from app.schemas import schemas
from app.services.street_service import interpolate_points
from typing import List

router = APIRouter()

@router.post("/streetlights/", response_model=schemas.StreetLight)
def create_street_light(request: schemas.StreetLightCreate, db: Session = Depends(get_db)):
    db_street_light = models.StreetLight(
        latitude=street_light.latitude,
        longitude=street_light.longitude,
        address=street_light.address,
        ward=street_light.ward,
        street_id=street_light.street_id,
    )

    db.add(db_street_light)
    db.commit()
    db.refresh(db_street_light)

    if street_light.installation_detail:
        installation_detail = models.InstallationDetail(
            street_light_id=db_street_light.id,
            **street_light.installation_detail.dict()
        )
        db.add(installation_detail)
    
    if street_light.light_specification:
        light_specification = models.LightSpecification(
            street_light_id=db_street_light.id,
            **street_light.light_specification.dict()
        )
        db.add(light_specification)

    if street_light.hardware_information:    
        hardware_information = models.HardwareInformation(
            street_light_id=db_street_light.id,
            **street_light.hardware_information.dict()
        )
        db.add(hardware_information)

    if street_light.warranties:   
        for warranty in street_light.warranties:
            db_warranty = models.WarrantyInformation(
                street_light_id=db_street_light.id,
                **warranty.dict()
            )
            db.add(db_warranty)
    
    if street_light.cost_pricing:
        cost_pricing = models.CostAndPricing(
            street_light_id=db_street_light.id,
            **street_light.cost_pricing.dict()
        )
        db.add(cost_pricing)

    if street_light.energy_consumption:
        energy_consumption = models.EnergyConsumption(
            street_light_id=db_street_light.id,
            **street_light.energy_consumption.dict()
        )
        db.add(energy_consumption)

    if street_light.operational_status:
        operational_status = models.OperationalStatus(
            street_light_id=db_street_light.id,
            **street_light.operational_status.dict()
        )
        db.add(operational_status)

    if street_light.life_cycle_information:
        life_cycle_information = models.LifeCycleInformation(
            street_light_id=db_street_light.id,
            **street_light.life_cycle_information.dict()
        )
        db.add(life_cycle_information)

    db.commit()
    return db_street_light

@router.get("/streetlights/{street_light_id}", response_model=schemas.StreetLight)
def get_street_light(street_light_id: int, db: Session = Depends(get_db)):
    street_light = db.query(models.StreetLight).filter(models.StreetLight.id == street_light_id).first()
    if not street_light:
        raise HTTPException(status_code=404, detail="Street Light not found")
    return street_light

@router.post("/interpolate-points", response_model=schemas.StreetPointsResponse)
def get_interpolated_points(request: schemas.StreetPointsRequest):
    points = interpolate_points(request.start_point, request.end_point, request.num_points)
    return StreetPointsResponse(points=points)

@router.post("/streetlights/operations/")
def create_street_light_operations(
    operations: List[schemas.StreetLightOperationCreate], db: Session = Depends(get_db)
):
    for operation in operations:
        db_operation = models.StreetLightOperation(
            street_light_id=operation.street_light_id,
            timestamp=operation.timestamp,
            power_consumption=operation.power_consumption,
            voltage_levels=operation.voltage_levels,
            current_fluctuations=operation.current_fluctuations,
            temperature=operation.temperature,
            environmental_conditions=operation.environmental_conditions,
            current_fluctuations_env=operation.current_fluctuations_env,
            fault_type=operation.fault_type,
        )
        db.add(db_operation)

    db.commit()
    return {"status": "success", "message": "Operations data ingested successfully"}

@router.get("/streetlights/{street_light_id}/operations/")
def get_street_light_operations(street_light_id: int, db: Session = Depends(get_db)):
    operations = db.query(models.StreetLightOperation).filter(
        models.StreetLightOperation.street_light_id == street_light_id
    ).all()

    if not operations:
        raise HTTPException(status_code=404, detail="No operations found for this street light")

    return operations

@router.get("/streetlights/faults/")
async def get_faulty_street_lights(db: Session = Depends(get_db)):
    faulty_lights = db.query(models.StreetLightOperation).filter(
        models.StreetLightOperation.fault_type != 0
    ).all()

    return faulty_lights
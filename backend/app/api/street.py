from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import models
from app.db import get_db
from app.schemas import schemas
from app.services.street_service import interpolate_points
from typing import List
from datetime import datetime, timedelta

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
    return schemas.StreetPointsResponse(points=points)

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

@router.get("/streets/{street_id}/basic", response_model=schemas.StreetBasicInfo)
def get_street_basic_info(street_id: int, db: Session = Depends(get_db)):
    street = db.query(models.Street).filter(models.Street.id == street_id).first()
    if not street:
        raise HTTPException(status_code=404, detail="Street not found")
    total_lights = db.query(func.count(models.StreetLight.id))\
        .filter(models.StreetLight.street_id == street_id)\
        .scalar()
    total_power = db.query(func.sum(models.EnergyConsumption.average_monthly_consumption))\
        .join(models.StreetLight)\
        .filter(models.StreetLight.street_id == street_id)\
        .scalar() or 0
    status_summary = db.query(
        models.OperationalStatus.current_status,
        func.count(models.OperationalStatus.id)
    ).join(models.StreetLight)\
        .filter(models.StreetLight.street_id == street_id)\
        .group_by(models.OperationalStatus.current_status)\
        .all()
    recent_issues = db.query(func.count(models.IssueReport.id))\
        .join(models.StreetLight)\
        .filter(
            models.StreetLight.street_id == street_id,
            models.IssueReport.issue_date >= datetime.now() - timedelta(days=30)
        ).scalar() or 0
    coordinates = None
    if street.start_latitude and street.start_longitude and street.end_latitude and street.end_longitude:
        coordinates = schemas.StreetLocation(
            start=schemas.Coordinates(
                latitude=street.start_latitude,
                longitude=street.start_longitude
            ),
            end=schemas.Coordinates(
                latitude=street.end_latitude,
                longitude=street.end_longitude
            )
        )
    return schemas.StreetBasicInfo(
        id=street.id,
        street_name=street.name,
        ward=street.ward,
        total_lights=total_lights,
        total_power_consumption=total_power,
        operational_summary={status: count for status, count in status_summary},
        recent_issues=recent_issues,
        coordinates=coordinates
    )

@router.get("/streets/{street_id}/detailed", response_model=schemas.StreetDetailedInfo)
def get_street_detailed_info(street_id: int, db: Session = Depends(get_db)):
    street = db.query(models.Street).filter(models.Street.id == street_id).first()
    if not street:
        raise HTTPException(status_code=404, detail="Street not found")
    lights = db.query(models.StreetLight)\
        .filter(models.StreetLight.street_id == street_id)\
        .all()
    light_ids = [light.id for light in lights]
    maintenance_history = db.query(models.MaintenanceHistory)\
        .filter(models.MaintenanceHistory.street_light_id.in_(light_ids))\
        .order_by(models.MaintenanceHistory.maintenance_date.desc())\
        .all()
    energy_data = db.query(models.EnergyConsumption)\
        .filter(models.EnergyConsumption.street_light_id.in_(light_ids))\
        .all()
    warranties = db.query(models.WarrantyInformation)\
        .filter(models.WarrantyInformation.street_light_id.in_(light_ids))\
        .all()
    costs = db.query(models.CostAndPricing)\
        .filter(models.CostAndPricing.street_light_id.in_(light_ids))\
        .all()
    total_installation_cost = sum(cost.installation_cost or 0 for cost in costs)
    total_maintenance_cost = sum(cost.maintenance_cost or 0 for cost in costs)
    total_electricity_cost = sum(cost.electricity_cost or 0 for cost in costs)
    return schemas.StreetDetailedInfo(
        street_info=schemas.StreetInfo(
            street_name=street.name,
            ward=street.ward,
            description=street.description
        ),
        lights_info=[
            schemas.LightInfo(
                id=light.id,
                location=schemas.Coordinates(
                    latitude=light.latitude,
                    longitude=light.longitude
                ),
                address=light.address,
                installation=schemas.LightInstallation(
                    installation_date=light.installation_detail.installation_date,
                    contractor_name=light.installation_detail.contractor_name
                ) if light.installation_detail else None,
                specifications=schemas.LightSpecification(
                    bulb_type=light.light_specification.bulb_type,
                    bulb_manufacturer=light.light_specification.bulb_manufacturer,
                    wattage=light.light_specification.wattage
                ) if light.light_specification else None,
                status=schemas.OperationalStatus(
                    current_status=light.operational_status.current_status,
                    last_status_update=light.operational_status.last_status_update
                ) if light.operational_status else None
            ) for light in lights
        ],
        maintenance_summary=schemas.MaintenanceSummary(
            total_maintenance_records=len(maintenance_history),
            maintenance=[
                schemas.MaintenanceRecord(
                    date=record.maintenance_date,
                    type=record.maintenance_type,
                    cost=record.cost,
                    street_light_id=record.street_light_id,
                )
                for record in maintenance_history
            ]
        ),
        energy_summary=schemas.EnergySummary(
            total_monthly_consumption=sum(e.average_monthly_consumption or 0 for e in energy_data),
            average_daily_consumption=sum(e.average_daily_consumption or 0 for e in energy_data) / len(energy_data) if energy_data else 0,
            per_light_consumption=[
                schemas.LightEnergyConsumption(
                    light_id=e.street_light_id,
                    monthly_consumption=e.average_monthly_consumption or 0,
                    daily_consumption=e.average_daily_consumption or 0
                )
                for e in energy_data
            ]
        ),
        cost_summary=schemas.CostSummary(
            total_installation_cost=total_installation_cost,
            total_maintenance_cost=total_maintenance_cost,
            total_electricity_cost=total_electricity_cost,
            total_cost=total_installation_cost + total_maintenance_cost + total_electricity_cost
        ),
        warranty_summary=schemas.WarrantySummary(
            active_warranties=len([w for w in warranties if w.warranty_end > datetime.now().date()]),
            expiring_soon=len([w for w in warranties if w.warranty_end > datetime.now().date() 
                                and w.warranty_end <= (datetime.now() + timedelta(days=90)).date()])
        )
    )

@router.get("/streets/list", response_model=List[schemas.StreetBasicInfo])
def get_all_streets(db: Session = Depends(get_db)):
    streets = db.query(models.Street).all()
    street_info_list = []
    for street in streets:
        total_lights = db.query(func.count(models.StreetLight.id))\
            .filter(models.StreetLight.street_id == street.id)\
            .scalar()
        total_power = db.query(func.sum(models.EnergyConsumption.average_monthly_consumption))\
            .join(models.StreetLight)\
            .filter(models.StreetLight.street_id == street.id)\
            .scalar() or 0
        status_summary = db.query(
            models.OperationalStatus.current_status,
            func.count(models.OperationalStatus.id)
        ).join(models.StreetLight)\
            .filter(models.StreetLight.street_id == street.id)\
            .group_by(models.OperationalStatus.current_status)\
            .all()
        recent_issues = db.query(func.count(models.IssueReport.id))\
            .join(models.StreetLight)\
            .filter(
                models.StreetLight.street_id == street.id,
                models.IssueReport.issue_date >= datetime.now() - timedelta(days=30)
            ).scalar() or 0
        coordinates = None
        if street.start_latitude and street.start_longitude and street.end_latitude and street.end_longitude:
            coordinates = schemas.StreetLocation(
                start=schemas.Coordinates(
                    latitude=street.start_latitude,
                    longitude=street.start_longitude
                ),
                end=schemas.Coordinates(
                    latitude=street.end_latitude,
                    longitude=street.end_longitude
                )
            )
        street_info = schemas.StreetBasicInfo(
            id=street.id,
            street_name=street.name,
            ward=street.ward,
            total_lights=total_lights,
            total_power_consumption=total_power,
            operational_summary={status: count for status, count in status_summary},
            recent_issues=recent_issues,
            coordinates=coordinates
        )
        street_info_list.append(street_info)
    return street_info_list
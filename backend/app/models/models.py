from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.db import DECLARATIVE_BASE as Base

class StreetLight(Base):
    __tablename__ = "street_lights"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String)
    ward = Column(String)
    street_id = Column(Integer, ForeignKey("streets.id"))

    installation_detail = relationship("InstallationDetail", uselist=False, back_populates="street_light")
    light_specification = relationship("LightSpecification", uselist=False, back_populates="street_light")
    hardware_information = relationship("HardwareInformation", uselist=False, back_populates="street_light")
    warranties = relationship("WarrantyInformation", back_populates="street_light")
    cost_pricing = relationship("CostAndPricing", uselist=False, back_populates="street_light")
    maintenance_histories = relationship("MaintenanceHistory", back_populates="street_light")
    issue_reports = relationship("IssueReport", back_populates="street_light")
    energy_consumption = relationship("EnergyConsumption", uselist=False, back_populates="street_light")
    operational_status = relationship("OperationalStatus", uselist=False, back_populates="street_light")
    life_cycle_information = relationship("LifeCycleInformation", uselist=False, back_populates="street_light")

    street = relationship("Street", back_populates="street_lights")


class InstallationDetail(Base):
    __tablename__ = "installation_details"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    installation_date = Column(Date, nullable=False)
    contractor_name = Column(String)

    street_light = relationship("StreetLight", back_populates="installation_detail")


class LightSpecification(Base):
    __tablename__ = "light_specifications"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    bulb_type = Column(String)
    bulb_manufacturer = Column(String)
    wattage = Column(Integer)

    street_light = relationship("StreetLight", back_populates="light_specification")


class HardwareInformation(Base):
    __tablename__ = "hardware_information"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    pole_type = Column(String)
    pole_height = Column(Float)
    control_system_type = Column(String)

    street_light = relationship("StreetLight", back_populates="hardware_information")


class WarrantyInformation(Base):
    __tablename__ = "warranty_information"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    component_name = Column(String)
    warranty_start = Column(Date)
    warranty_end = Column(Date)
    warranty_terms = Column(Text)

    street_light = relationship("StreetLight", back_populates="warranties")


class CostAndPricing(Base):
    __tablename__ = "cost_and_pricing"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    installation_cost = Column(Float)
    bulb_cost = Column(Float)
    fixture_cost = Column(Float)
    electricity_cost = Column(Float)
    maintenance_cost = Column(Float)

    street_light = relationship("StreetLight", back_populates="cost_pricing")


class MaintenanceHistory(Base):
    __tablename__ = "maintenance_history"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    maintenance_date = Column(Date)
    maintenance_type = Column(String)
    cost = Column(Float)
    contractor_name = Column(String)
    notes = Column(Text)

    street_light = relationship("StreetLight", back_populates="maintenance_histories")


class IssueReport(Base):
    __tablename__ = "issue_reports"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    issue_date = Column(Date)
    issue_description = Column(Text)
    resolution_status = Column(String)
    resolution_date = Column(Date)
    time_to_resolve = Column(Float)  # In hours

    street_light = relationship("StreetLight", back_populates="issue_reports")


class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    average_daily_consumption = Column(Float)
    average_monthly_consumption = Column(Float)
    operating_hours = Column(Integer)

    street_light = relationship("StreetLight", back_populates="energy_consumption")


class OperationalStatus(Base):
    __tablename__ = "operational_status"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    current_status = Column(String)
    last_status_update = Column(Date)

    street_light = relationship("StreetLight", back_populates="operational_status")


class LifeCycleInformation(Base):
    __tablename__ = "life_cycle_information"

    id = Column(Integer, primary_key=True, index=True)
    street_light_id = Column(Integer, ForeignKey("street_lights.id"))
    component = Column(String)
    expected_lifespan = Column(Integer)  # In years
    replacement_schedule = Column(Date)

    street_light = relationship("StreetLight", back_populates="life_cycle_information")


class Street(Base):
    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_latitude = Column(Float, nullable=False)
    start_longitude = Column(Float, nullable=False)
    end_latitude = Column(Float)
    end_longitude = Column(Float)
    description = Column(String)
    ward = Column(String)

    street_lights = relationship("StreetLight", back_populates="street")
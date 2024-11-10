from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Get database URL from environment variables."""
    POSTGRES_USER = os.getenv('STREET_SMART_DATABASE_USER', 'default_user')
    POSTGRES_PASSWORD = os.getenv('STREET_SMART_DATABASE_PASSWORD', 'default_password')
    POSTGRES_DB = os.getenv('STREET_SMART_DATABASE_NAME', 'default_db')
    POSTGRES_HOST = os.getenv('STREET_SMART_DATABASE_HOST', 'localhost')
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

STREET_START = (77.0521098621715, 28.596682537282675)
STREET_END = (77.0544098621715, 28.595122537282675)
NUM_LIGHTS = 10

DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def interpolate_points(start: tuple, end: tuple, num_points: int) -> list:
    """Generate evenly spaced points between start and end coordinates."""
    lats = np.linspace(start[1], end[1], num_points)
    longs = np.linspace(start[0], end[0], num_points)
    return [(float(lon), float(lat)) for lon, lat in zip(longs, lats)]

def generate_data():
    """Generate and insert dummy data for street lights."""
    db = SessionLocal()
    try:
        street_query = text("""
            INSERT INTO streets (name, start_latitude, start_longitude, 
            end_latitude, end_longitude, description, ward) 
            VALUES (:name, :start_latitude, :start_longitude, 
            :end_latitude, :end_longitude, :description, :ward) 
            RETURNING id
        """)
        
        street_result = db.execute(
            street_query,
            {
                'name': 'Central Avenue',
                'start_latitude': float(STREET_START[1]),
                'start_longitude': float(STREET_START[0]),
                'end_latitude': float(STREET_END[1]),
                'end_longitude': float(STREET_END[0]),
                'description': 'Main street with smart LED lighting',
                'ward': 'Central Ward'
            }
        )
        street_id = street_result.scalar()
        
        points = interpolate_points(STREET_START, STREET_END, NUM_LIGHTS)
        base_date = datetime(2023, 1, 1)
        
        for i, (longitude, latitude) in enumerate(points):
            light_query = text("""
                INSERT INTO street_lights (latitude, longitude, address, ward, street_id)
                VALUES (:latitude, :longitude, :address, :ward, :street_id)
                RETURNING id
            """)
            
            light_result = db.execute(
                light_query,
                {
                    'latitude': latitude,  
                    'longitude': longitude,
                    'address': f'Light {i+1}, Central Avenue',
                    'ward': 'Central Ward',
                    'street_id': street_id
                }
            )
            light_id = light_result.scalar()
            
            install_date = base_date + timedelta(days=i*2)
            db.execute(
                text("""
                    INSERT INTO installation_details 
                    (street_light_id, installation_date, contractor_name)
                    VALUES (:light_id, :date, :contractor)
                """),
                {
                    'light_id': light_id,
                    'date': install_date,
                    'contractor': 'Smart City Contractors Ltd.'
                }
            )
            
            db.execute(
                text("""
                    INSERT INTO light_specifications 
                    (street_light_id, bulb_type, bulb_manufacturer, wattage)
                    VALUES (:light_id, :type, :manufacturer, :wattage)
                """),
                {
                    'light_id': light_id,
                    'type': 'LED',
                    'manufacturer': 'Philips',
                    'wattage': 90
                }
            )

            db.execute(
                text("""
                    INSERT INTO hardware_information 
                    (street_light_id, pole_type, pole_height, control_system_type)
                    VALUES (:light_id, :pole_type, :height, :control)
                """),
                {
                    'light_id': light_id,
                    'pole_type': 'Galvanized Steel',
                    'height': 9.0,
                    'control': 'Smart Controller'
                }
            )

            for component in ['LED Module', 'Driver', 'Pole']:
                db.execute(
                    text("""
                        INSERT INTO warranty_information 
                        (street_light_id, component_name, warranty_start, warranty_end, warranty_terms)
                        VALUES (:light_id, :component, :start, :end, :terms)
                    """),
                    {
                        'light_id': light_id,
                        'component': component,
                        'start': install_date,
                        'end': install_date + timedelta(days=365*5),
                        'terms': f'5-year standard warranty for {component}'
                    }
                )

            db.execute(
                text("""
                    INSERT INTO cost_and_pricing 
                    (street_light_id, installation_cost, bulb_cost, fixture_cost, 
                    electricity_cost, maintenance_cost)
                    VALUES (:light_id, :install, :bulb, :fixture, :electricity, :maintenance)
                """),
                {
                    'light_id': light_id,
                    'install': 12000.0,
                    'bulb': 1500.0,
                    'fixture': 3500.0,
                    'electricity': 180.0,
                    'maintenance': 1200.0
                }
            )

            db.execute(
                text("""
                    INSERT INTO energy_consumption 
                    (street_light_id, average_daily_consumption, 
                    average_monthly_consumption, operating_hours)
                    VALUES (:light_id, :daily, :monthly, :hours)
                """),
                {
                    'light_id': light_id,
                    'daily': 1.8,
                    'monthly': 54.0,
                    'hours': 12
                }
            )

            db.execute(
                text("""
                    INSERT INTO operational_status 
                    (street_light_id, current_status, last_status_update)
                    VALUES (:light_id, :status, :update)
                """),
                {
                    'light_id': light_id,
                    'status': 'Operational',
                    'update': datetime.now().date()
                }
            )

            db.execute(
                text("""
                    INSERT INTO life_cycle_information 
                    (street_light_id, component, expected_lifespan, replacement_schedule)
                    VALUES (:light_id, :component, :lifespan, :schedule)
                """),
                {
                    'light_id': light_id,
                    'component': 'LED Module',
                    'lifespan': 8,
                    'schedule': install_date + timedelta(days=365*8)
                }
            )

            db.execute(
                text("""
                    INSERT INTO maintenance_history 
                    (street_light_id, maintenance_date, maintenance_type, 
                    cost, contractor_name, notes)
                    VALUES (:light_id, :date, :type, :cost, :contractor, :notes)
                """),
                {
                    'light_id': light_id,
                    'date': install_date + timedelta(days=90),
                    'type': 'Routine Inspection',
                    'cost': 800.0,
                    'contractor': 'Maintenance Corp',
                    'notes': 'Regular quarterly maintenance'
                }
            )

            if i % 3 == 0:
                issue_date = install_date + timedelta(days=120)
                db.execute(
                    text("""
                        INSERT INTO issue_reports 
                        (street_light_id, issue_date, issue_description, 
                        resolution_status, resolution_date, time_to_resolve)
                        VALUES (:light_id, :issue_date, :issue_description, 
                        :resolution_status, :resolution_date, :time_to_resolve)
                    """),
                    {
                        'light_id': light_id,
                        'issue_date': issue_date,
                        'issue_description': 'Flickering observed during night hours',
                        'resolution_status': 'Resolved',
                        'resolution_date': issue_date + timedelta(days=2),
                        'time_to_resolve': 48.0
                    }
                )
        db.commit()
        print("Data generation completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error generating data: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    generate_data()
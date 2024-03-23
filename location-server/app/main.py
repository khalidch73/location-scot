from contextlib import asynccontextmanager
from typing import Annotated, List
from app import settings 
from sqlmodel import Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends, HTTPException, Path
from app.models import LocationFinder, CreateLocationRequest
from pydantic import BaseModel
from typing import Optional


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Location Finder API", 
    version="0.0.1",
    servers=[
        {
            "url": "https://b573-223-123-103-122.ngrok-free.app", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session

# 01 Define the route to read route
@app.get("/")
def read_root():
    return {"Welcome": "Location Finder"}


# 02 Define the route to create a location
@app.post("/locations/", response_model=LocationFinder)
async def create_location(location_request: CreateLocationRequest, session: Session = Depends(get_session)):
    # Create a new LocationFinder instance with data from the request
    new_location = LocationFinder(name=location_request.name, location=location_request.location)
    # Add the new location to the session and commit the transaction
    session.add(new_location)
    session.commit()
    # Refresh the instance to get database-assigned values
    session.refresh(new_location)
    # Return the created location
    return new_location

# 03 Define the route to read a location by its name
@app.get("/locations/{location_name}", response_model=LocationFinder)
async def read_location(location_name: str, session: Session = Depends(get_session)):
    # Query the database to find the location by its name
    location = session.exec(select(LocationFinder).where(LocationFinder.name == location_name)).first()

    # If location is not found, raise HTTPException with 404 status code
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    # Return the location
    return location


# 04 Define the route to delete a location by its name
@app.delete("/locations/{location_name}")
async def delete_location(location_name: str, session: Session = Depends(get_session)):
    # Query the database to find the location by its name
    location = session.exec(select(LocationFinder).where(LocationFinder.name == location_name)).first()

    # If location is not found, raise HTTPException with 404 status code
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    # Delete the location from the database
    session.delete(location)
    session.commit()

    # Return a message indicating successful deletion
    return {"message": f"Location '{location_name}' deleted successfully"}

# 05 Define the route to update a location by its name
@app.put("/locations/{location_name}")
async def update_location(location_name: str, updated_location: LocationFinder, session: Session = Depends(get_session)):
    # Query the database to find the location by its name
    location = session.exec(select(LocationFinder).where(LocationFinder.name == location_name)).first()

    # If location is not found, raise HTTPException with 404 status code
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    # Update the location data
    location.location = updated_location.location

    # Commit the changes to the database
    session.commit()

    # Return a message indicating successful update
    return {"message": f"Location of '{location_name}' updated successfully"}

# 06 Define the route to read all locations
@app.get("/locations/", response_model=List[LocationFinder])
async def read_all_locations(session: Session = Depends(get_session)):
    # Query the database to retrieve all locations
    locations = session.exec(select(LocationFinder)).all()

    # Return the list of locations
    return locations

# 07 Define the route to delete all locations
@app.delete("/locations/")
async def delete_all_locations(session: Session = Depends(get_session)):
    # Query the database to retrieve all locations
    locations = session.exec(select(LocationFinder)).all()

    # If no locations are found, raise HTTPException with 404 status code
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found")

    # Delete all locations from the database
    for location in locations:
        session.delete(location)
    session.commit()

    # Return a message indicating successful deletion
    return {"message": "All locations deleted successfully"}
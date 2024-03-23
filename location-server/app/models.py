from sqlmodel import Field, SQLModel 
from pydantic import BaseModel
from typing import Optional

class LocationFinder(SQLModel, table=True):
    name: str = Field(index=True, primary_key=True, default='')
    location: str = Field(index=True, default='')

# Define a Pydantic model for the request
class CreateLocationRequest(BaseModel):
    name: str
    location: Optional[str] = None

from pydantic import BaseModel
from typing import List

class StreetPointsRequest(BaseModel):
    start_point: List[float]
    end_point: List[float]
    num_points: int

class StreetPointsResponse(BaseModel):
    points: List[List[float]]

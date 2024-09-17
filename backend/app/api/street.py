from fastapi import APIRouter
from app.models.street import StreetPointsRequest, StreetPointsResponse
from app.services.street_service import interpolate_points

router = APIRouter()

@router.post("/interpolate-points", response_model=StreetPointsResponse)
def get_interpolated_points(request: StreetPointsRequest):
    points = interpolate_points(request.start_point, request.end_point, request.num_points)
    return StreetPointsResponse(points=points)

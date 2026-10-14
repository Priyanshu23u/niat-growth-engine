"""
API Router: Financial ROI & Education Loan EMI Calculator
"""

from fastapi import APIRouter
from backend.app.schemas.roi import RoiSimulationInput, RoiResponse
from backend.app.services.roi_calculator import calculate_roi_model

router = APIRouter(prefix="/api/roi", tags=["ROI Simulator"])


@router.post("", response_model=RoiResponse)
def compute_roi(body: RoiSimulationInput):
    """
    Computes custom 5-year career financial return, monthly EMI, and break-even months.
    """
    result = calculate_roi_model(body)
    return result


@router.get("", response_model=RoiResponse)
def get_default_roi():
    """
    Returns baseline ROI projection comparing NIAT against standard tier-3 college.
    """
    default_result = calculate_roi_model()
    return default_result

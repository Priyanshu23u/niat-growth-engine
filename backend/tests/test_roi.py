"""
Unit Tests: Financial ROI & Loan EMI Calculator
"""

import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app.schemas.roi import RoiSimulationInput
from backend.app.services.roi_calculator import calculate_roi_model


def test_default_roi_calculation():
    result = calculate_roi_model()
    assert result["success"] is True

    metrics = result["metrics"]
    assert 0 < metrics["breakEvenMonths"] <= 30, f"Break-even must be realistic, got {metrics['breakEvenMonths']} months"
    assert metrics["fiveYearNetWealthAdvantage"] > 1000000, "5-year wealth delta must be > ₹10 Lakhs"

    inputs = result["inputs"]
    assert 12000 < inputs["monthlyEmi"] < 18000, f"Expected realistic EMI, got ₹{inputs['monthlyEmi']}"

    projections = result["yearlyProjections"]
    assert len(projections) == 5, "Must produce 5 annual projection rows"

    # Cumulative wealth must increase year over year
    assert projections[4]["niatNetCumulativeWealth"] > projections[0]["niatNetCumulativeWealth"]


def test_custom_roi_simulation():
    custom_input = RoiSimulationInput(
        niatTotalFee=1400000,
        tier3TotalFee=400000,
        niatExpectedStartingSalary=1000000,
        tier3ExpectedStartingSalary=360000,
        loanSharePercentage=70.0,
        loanInterestRate=8.5,
        loanTenureYears=5,
        annualSalaryHike=18.0,
    )
    result = calculate_roi_model(custom_input)
    assert result["success"] is True
    assert result["metrics"]["breakEvenMonths"] > 0
    assert result["metrics"]["fiveYearNetWealthAdvantage"] > 2000000

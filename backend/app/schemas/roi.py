"""
Pydantic Schemas for Financial ROI Simulator
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RoiSimulationInput(BaseModel):
    niatTotalFee: Optional[int] = Field(1200000, description="4-Year NIAT Total Program Investment in INR")
    tier3TotalFee: Optional[int] = Field(400000, description="4-Year Tier-3 Local College Fee in INR")
    niatExpectedStartingSalary: Optional[int] = Field(850000, description="NIAT Target Starting Salary LPA in INR")
    tier3ExpectedStartingSalary: Optional[int] = Field(360000, description="Tier-3 Target Starting Salary LPA in INR")
    loanSharePercentage: Optional[float] = Field(60.0, description="Percentage of fee funded by education loan")
    loanInterestRate: Optional[float] = Field(8.5, description="Annual education loan interest rate (SBI/HDFC)")
    loanTenureYears: Optional[int] = Field(5, description="Loan repayment tenure in years")
    annualSalaryHike: Optional[float] = Field(15.0, description="Expected annual tech salary hike %")


class YearlyProjection(BaseModel):
    year: int
    niatGrossSalary: int
    tier3GrossSalary: int
    salaryDelta: int
    annualLoanEmi: int
    niatNetCumulativeWealth: int
    tier3NetCumulativeWealth: int
    netWealthAdvantage: int


class RoiMetrics(BaseModel):
    breakEvenMonths: int
    breakEvenYears: str
    fiveYearNetWealthAdvantage: int
    salaryAdvantageYear1: int
    salaryAdvantageYear5: int
    roiMultiplier: str


class RoiResponse(BaseModel):
    success: bool
    inputs: Dict[str, Any]
    metrics: RoiMetrics
    yearlyProjections: List[YearlyProjection]

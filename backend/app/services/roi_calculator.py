"""
ROI Calculator Service — Financial Modeling and Loan EMI Projection
"""

import math
from typing import Dict, Any, Optional
from backend.app.schemas.roi import RoiSimulationInput, RoiResponse, RoiMetrics, YearlyProjection


def calculate_roi_model(input_data: Optional[RoiSimulationInput] = None) -> Dict[str, Any]:
    """
    Computes 5-year career financial return on investment comparing
    NIAT against a traditional local tier-3 engineering college.
    """
    if input_data is None:
        input_data = RoiSimulationInput()

    niat_fee = input_data.niatTotalFee or 1200000
    tier3_fee = input_data.tier3TotalFee or 400000
    niat_salary = input_data.niatExpectedStartingSalary or 850000
    tier3_salary = input_data.tier3ExpectedStartingSalary or 360000
    loan_share = (input_data.loanSharePercentage if input_data.loanSharePercentage is not None else 60.0) / 100.0
    interest_rate = (input_data.loanInterestRate if input_data.loanInterestRate is not None else 8.5) / 100.0
    loan_tenure = input_data.loanTenureYears if input_data.loanTenureYears is not None else 5
    hike_rate = (input_data.annualSalaryHike if input_data.annualSalaryHike is not None else 15.0) / 100.0

    # 1. Education loan EMI calculation
    loan_principal = niat_fee * loan_share
    monthly_rate = interest_rate / 12.0
    total_months = loan_tenure * 12

    if monthly_rate == 0 or total_months == 0:
        monthly_emi = round(loan_principal / total_months) if total_months > 0 else 0
    else:
        compound_factor = math.pow(1.0 + monthly_rate, total_months)
        monthly_emi = round((loan_principal * monthly_rate * compound_factor) / (compound_factor - 1.0))

    total_loan_repayment = monthly_emi * total_months
    total_interest_paid = total_loan_repayment - loan_principal

    # 2. 5-Year Post-Graduation Career Earnings Projection
    yearly_projections = []
    niat_cumulative = -niat_fee
    tier3_cumulative = -tier3_fee

    current_niat_salary = float(niat_salary)
    current_tier3_salary = float(tier3_salary)

    for year in range(1, 6):
        niat_post_tax = current_niat_salary * 0.88
        tier3_post_tax = current_tier3_salary * 0.94

        annual_emi_deduction = (monthly_emi * 12) if year <= loan_tenure else 0
        niat_net_yearly = niat_post_tax - annual_emi_deduction

        niat_cumulative += niat_net_yearly
        tier3_cumulative += tier3_post_tax

        yearly_projections.append({
            "year": year,
            "niatGrossSalary": round(current_niat_salary),
            "tier3GrossSalary": round(current_tier3_salary),
            "salaryDelta": round(current_niat_salary - current_tier3_salary),
            "annualLoanEmi": annual_emi_deduction,
            "niatNetCumulativeWealth": round(niat_cumulative),
            "tier3NetCumulativeWealth": round(tier3_cumulative),
            "netWealthAdvantage": round(niat_cumulative - tier3_cumulative),
        })

        current_niat_salary *= (1.0 + hike_rate)
        current_tier3_salary *= (1.0 + 0.07)  # standard 7% services increment

    # 3. Break-even payback calculation
    fee_delta = (niat_fee - tier3_fee) + total_interest_paid
    monthly_starting_salary_delta = (niat_salary - tier3_salary) / 12.0
    break_even_months = max(12, round(fee_delta / monthly_starting_salary_delta)) if monthly_starting_salary_delta > 0 else 36

    five_year_net_wealth_advantage = yearly_projections[-1]["netWealthAdvantage"]
    roi_multiplier = f"{(yearly_projections[-1]['niatGrossSalary'] * 5 / niat_fee):.2f}"

    return {
        "success": True,
        "inputs": {
            "niatTotalFee": niat_fee,
            "tier3TotalFee": tier3_fee,
            "niatStartingLpa": niat_salary,
            "tier3StartingLpa": tier3_salary,
            "loanPrincipal": round(loan_principal),
            "monthlyEmi": monthly_emi,
            "totalLoanRepayment": total_loan_repayment,
            "totalInterestPaid": round(total_interest_paid),
        },
        "metrics": {
            "breakEvenMonths": break_even_months,
            "breakEvenYears": f"{(break_even_months / 12.0):.1f}",
            "fiveYearNetWealthAdvantage": five_year_net_wealth_advantage,
            "salaryAdvantageYear1": niat_salary - tier3_salary,
            "salaryAdvantageYear5": yearly_projections[-1]["salaryDelta"],
            "roiMultiplier": roi_multiplier,
        },
        "yearlyProjections": yearly_projections,
    }

// ROI Model Calculator — ported from TypeScript to CommonJS

function calculateRoiModel(input = {}) {
  const niatTotalFee = input.niatTotalFee || 1200000;
  const tier3TotalFee = input.tier3TotalFee || 400000;
  const niatStartingLpa = input.niatExpectedStartingSalary || 850000;
  const tier3StartingLpa = input.tier3ExpectedStartingSalary || 360000;
  const loanShare = ((input.loanSharePercentage !== undefined ? input.loanSharePercentage : 60)) / 100;
  const interestRate = ((input.loanInterestRate !== undefined ? input.loanInterestRate : 8.5)) / 100;
  const loanTenure = input.loanTenureYears !== undefined ? input.loanTenureYears : 5;
  const hikeRate = ((input.annualSalaryHike !== undefined ? input.annualSalaryHike : 15)) / 100;

  // Education Loan calculation
  const loanPrincipal = niatTotalFee * loanShare;
  const monthlyRate = interestRate / 12;
  const totalMonths = loanTenure * 12;
  const monthlyEmi =
    monthlyRate === 0
      ? Math.round(loanPrincipal / totalMonths)
      : Math.round(
          (loanPrincipal * monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) /
            (Math.pow(1 + monthlyRate, totalMonths) - 1)
        );

  const totalLoanRepayment = monthlyEmi * totalMonths;
  const totalInterestPaid = totalLoanRepayment - loanPrincipal;

  // 5-Year post-graduation career earnings projection
  const yearlyProjections = [];
  let niatCumulative = -niatTotalFee;
  let tier3Cumulative = -tier3TotalFee;

  let currentNiatSalary = niatStartingLpa;
  let currentTier3Salary = tier3StartingLpa;

  for (let year = 1; year <= 5; year++) {
    const niatPostTaxEstimate = currentNiatSalary * 0.88;
    const tier3PostTaxEstimate = currentTier3Salary * 0.94;

    const annualEmiDeduction = year <= loanTenure ? monthlyEmi * 12 : 0;
    const niatNetYearly = niatPostTaxEstimate - annualEmiDeduction;

    niatCumulative += niatNetYearly;
    tier3Cumulative += tier3PostTaxEstimate;

    yearlyProjections.push({
      year,
      niatGrossSalary: Math.round(currentNiatSalary),
      tier3GrossSalary: Math.round(currentTier3Salary),
      salaryDelta: Math.round(currentNiatSalary - currentTier3Salary),
      annualLoanEmi: annualEmiDeduction,
      niatNetCumulativeWealth: Math.round(niatCumulative),
      tier3NetCumulativeWealth: Math.round(tier3Cumulative),
      netWealthAdvantage: Math.round(niatCumulative - tier3Cumulative),
    });

    currentNiatSalary *= 1 + hikeRate;
    currentTier3Salary *= 1 + 0.07;
  }

  // Break-even month estimation
  const feeDelta = niatTotalFee - tier3TotalFee + totalInterestPaid;
  const monthlyStartingSalaryDelta = (niatStartingLpa - tier3StartingLpa) / 12;
  const breakEvenMonths = Math.max(12, Math.round(feeDelta / monthlyStartingSalaryDelta));

  return {
    inputs: {
      niatTotalFee,
      tier3TotalFee,
      niatStartingLpa,
      tier3StartingLpa,
      loanPrincipal,
      monthlyEmi,
      totalLoanRepayment,
      totalInterestPaid,
    },
    metrics: {
      breakEvenMonths,
      breakEvenYears: (breakEvenMonths / 12).toFixed(1),
      fiveYearNetWealthAdvantage: yearlyProjections[4].netWealthAdvantage,
      salaryAdvantageYear1: niatStartingLpa - tier3StartingLpa,
      salaryAdvantageYear5: yearlyProjections[4].salaryDelta,
      roiMultiplier: ((yearlyProjections[4].niatGrossSalary * 5) / niatTotalFee).toFixed(2),
    },
    yearlyProjections,
  };
}

module.exports = { calculateRoiModel };

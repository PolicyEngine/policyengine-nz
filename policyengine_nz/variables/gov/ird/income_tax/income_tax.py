"""Income tax calculation for New Zealand residents."""

from policyengine_nz.model_api import *


class income_tax(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Income tax"
    documentation = "Total income tax liability for New Zealand residents"
    reference = "https://www.ird.govt.nz/income-tax/income-tax-for-individuals/tax-codes-and-tax-rates-for-individuals/tax-rates-for-individuals"
    unit = NZD

    def formula(person, period, parameters):
        taxable_income = person("taxable_income", period)
        p = parameters(period).gov.ird.income_tax

        # Get thresholds and rates
        thresholds = p.thresholds.thresholds
        rates = p.rates.rates

        # Initialize tax calculation
        tax = 0

        # Bracket 1: 0% up to tax-free threshold (currently $0)
        # No tax on first bracket as threshold is $0

        # Bracket 2: 10.5% on income from $0/$15,601 to $14,000/$53,500
        bracket_2_start = thresholds.bracket_2
        bracket_2_end = thresholds.bracket_3
        bracket_2_rate = rates.bracket_2

        if taxable_income > bracket_2_start:
            bracket_2_income = min_(
                taxable_income - bracket_2_start,
                bracket_2_end - bracket_2_start,
            )
            tax += bracket_2_income * bracket_2_rate

        # Bracket 3: 17.5% on income from $14,001/$53,501 to $48,000/$78,100
        bracket_3_start = thresholds.bracket_3
        bracket_3_end = thresholds.bracket_4
        bracket_3_rate = rates.bracket_3

        if taxable_income > bracket_3_start:
            bracket_3_income = min_(
                taxable_income - bracket_3_start,
                bracket_3_end - bracket_3_start,
            )
            tax += bracket_3_income * bracket_3_rate

        # Bracket 4: 30% on income from $48,001/$78,101 to $70,000/$180,000
        bracket_4_start = thresholds.bracket_4
        bracket_4_end = thresholds.bracket_5
        bracket_4_rate = rates.bracket_4

        if taxable_income > bracket_4_start:
            bracket_4_income = min_(
                taxable_income - bracket_4_start,
                bracket_4_end - bracket_4_start,
            )
            tax += bracket_4_income * bracket_4_rate

        # Bracket 5: 39% on income from $180,001 and above
        bracket_5_start = thresholds.bracket_5
        bracket_5_rate = rates.bracket_5

        if taxable_income > bracket_5_start:
            bracket_5_income = taxable_income - bracket_5_start
            tax += bracket_5_income * bracket_5_rate

        return tax

"""Investment income for New Zealand tax calculations."""

from policyengine_nz.model_api import *


class investment_income(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Investment income"
    documentation = "Income from dividends, interest, and other investments"
    reference = "https://www.ird.govt.nz/income-tax/income-tax-for-individuals/types-of-income/investment-income"
    unit = NZD

"""Self-employment income for New Zealand tax calculations."""

from policyengine_nz.model_api import *


class self_employment_income(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Self-employment income"
    documentation = (
        "Income from self-employment, business, and sole trader activities"
    )
    reference = "https://www.ird.govt.nz/income-tax/income-tax-for-individuals/types-of-income/self-employed-income"
    unit = NZD

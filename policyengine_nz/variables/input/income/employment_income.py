"""Employment income for New Zealand tax calculations."""

from policyengine_nz.model_api import *


class employment_income(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Employment income"
    documentation = "Income from wages, salaries, and employment"
    reference = "https://www.ird.govt.nz/income-tax/income-tax-for-individuals"
    unit = NZD
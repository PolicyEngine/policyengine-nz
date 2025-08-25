"""Taxable income calculation for New Zealand residents."""

from policyengine_nz.model_api import *


class taxable_income(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Taxable income"
    documentation = "Total taxable income for New Zealand income tax purposes"
    reference = "https://www.ird.govt.nz/income-tax/income-tax-for-individuals/working-out-your-income-tax"
    unit = NZD

    def formula(person, period, parameters):
        return (
            person("employment_income", period)
            + person("self_employment_income", period)
            + person("investment_income", period)
            # Additional income sources can be added here
        )

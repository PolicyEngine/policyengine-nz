"""ACC Earner's Levy calculation for New Zealand employees."""

from policyengine_nz.model_api import *


class acc_earners_levy(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "ACC Earner's Levy"
    documentation = "Annual ACC Earner's Levy paid on employment income"
    reference = [
        "https://www.acc.co.nz/for-business/acclevy/",
        "https://www.ird.govt.nz/roles/employers/paye-and-deductions/deductions/acc-earners-levy",
    ]
    unit = NZD

    def formula(person, period, parameters):
        employment_income = person("employment_income", period)
        p = parameters(period).gov.ird.acc

        # Get ACC levy parameters
        levy_rate = p.earners_levy_rate
        income_cap = p.earners_levy_cap

        # Calculate levy on employment income up to the cap
        liable_income = min_(employment_income, income_cap)

        return liable_income * levy_rate

"""Income liable for ACC Earner's Levy."""

from policyengine_nz.model_api import *


class acc_liable_income(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "ACC liable income"
    documentation = "Income subject to ACC Earner's Levy (capped at maximum)"
    reference = "https://www.acc.co.nz/for-business/acclevy/"
    unit = NZD
    
    def formula(person, period, parameters):
        employment_income = person("employment_income", period)
        p = parameters(period).gov.ird.acc
        
        # Apply the income cap for ACC levy purposes
        income_cap = p.earners_levy_cap
        
        return min_(employment_income, income_cap)
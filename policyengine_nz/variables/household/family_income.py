"""Family income for Working for Families calculations."""

from policyengine_nz.model_api import *


class family_income(Variable):
    value_type = float
    entity = Family
    definition_period = YEAR
    label = "Family income"
    documentation = "Combined annual income of all family members for Working for Families purposes"
    reference = "https://www.ird.govt.nz/working-for-families/eligibility/income-test"
    unit = NZD
    
    def formula(family, period, parameters):
        return family.sum(family.members("taxable_income", period))
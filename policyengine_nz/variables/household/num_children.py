"""Number of children in family for Working for Families calculations."""

from policyengine_nz.model_api import *


class num_children(Variable):
    value_type = int
    entity = Family
    definition_period = YEAR
    label = "Number of children"
    documentation = "Number of dependent children in the family"
    reference = "https://www.ird.govt.nz/working-for-families/eligibility"

    def formula(family, period, parameters):
        return family.sum(family.members("is_child", period))

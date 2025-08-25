"""Child status for New Zealand benefit calculations."""

from policyengine_nz.model_api import *


class is_child(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Is child"
    documentation = "Whether person is considered a dependent child"
    reference = "https://www.ird.govt.nz/working-for-families/eligibility"

    def formula(person, period, parameters):
        age = person("age", period)
        return age < 18

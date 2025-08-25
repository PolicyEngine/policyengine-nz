"""Age variable for New Zealand calculations."""

from policyengine_nz.model_api import *


class age(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR
    label = "Age"
    documentation = "Age in years as of the end of the tax year (31 March)"
    reference = "https://www.ird.govt.nz/income-tax/income-tax-for-individuals"

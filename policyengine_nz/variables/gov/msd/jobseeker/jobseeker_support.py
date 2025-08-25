"""Jobseeker Support payment calculation."""

from policyengine_nz.model_api import *


class receiving_jobseeker_support(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Receiving Jobseeker Support"
    documentation = "Whether person is receiving Jobseeker Support benefit"
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/jobseeker-support.html"


class is_sole_parent(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Is sole parent"
    documentation = "Whether person is a sole parent for benefit purposes"
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/sole-parent-support.html"


class has_partner(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Has partner"
    documentation = "Whether person has a partner/spouse for benefit purposes"


class jobseeker_support(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Jobseeker Support"
    documentation = "Annual Jobseeker Support benefit payment"
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/jobseeker-support.html"
    unit = NZD
    
    def formula(person, period, parameters):
        # Check eligibility
        receiving_jobseeker = person("receiving_jobseeker_support", period)
        age = person("age", period)
        has_partner = person("has_partner", period)
        is_sole_parent = person("is_sole_parent", period)
        
        # Get payment rates
        p = parameters(period).gov.msd.jobseeker.payment_rates.rates
        
        # Determine rate based on circumstances
        rate_weekly = select([
            is_sole_parent,
            (age >= 18) * (age <= 24) * not_(has_partner),
            (age >= 25) * not_(has_partner),
            has_partner  # Simplified - would need to check if partner also eligible
        ], [
            p.sole_parent,
            p.single_18_24,
            p.single_25_plus,
            p.couple_one_eligible  # Simplified - using one eligible rate
        ], default=0)
        
        # Convert to annual amount
        annual_amount = rate_weekly * WEEKS_IN_YEAR
        
        return where(receiving_jobseeker, annual_amount, 0)
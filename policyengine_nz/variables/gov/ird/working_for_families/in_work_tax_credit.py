"""In-Work Tax Credit calculation for Working for Families."""

from policyengine_nz.model_api import *


class work_hours_per_week(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Work hours per week"
    documentation = "Average hours worked per week"
    reference = "https://www.ird.govt.nz/working-for-families/types/in-work-tax-credit"


class in_work_tax_credit(Variable):
    value_type = float
    entity = Family
    definition_period = YEAR
    label = "In-Work Tax Credit"
    documentation = "Annual In-Work Tax Credit payment under Working for Families"
    reference = "https://www.ird.govt.nz/working-for-families/types/in-work-tax-credit"
    unit = NZD
    
    def formula(family, period, parameters):
        # Get family parameters
        num_children = family("num_children", period)
        num_parents = family.sum(
            family.members("age", period) >= 18
        )
        
        # Calculate total work hours for the family
        total_work_hours = family.sum(
            family.members("work_hours_per_week", period)
        )
        
        # Get parameters
        p = parameters(period).gov.ird.working_for_families.in_work_tax_credit
        
        # Determine minimum hours requirement
        is_single_parent = num_parents == 1
        min_hours_required = where(
            is_single_parent,
            p.work_hours.minimum_hours_single,
            p.work_hours.minimum_hours_couple
        )
        
        # Check work hours eligibility
        meets_work_hours = total_work_hours >= min_hours_required
        
        # Calculate IWTC amount
        base_rate = p.rates.base_rate
        additional_rate = p.rates.additional_child_rate
        
        # Base rate for families with 1-3 children
        # Additional rate for each child beyond 3
        children_base = min_(num_children, 3)
        children_additional = max_(0, num_children - 3)
        
        iwtc_amount = (
            base_rate +  # Base rate applies to all eligible families
            children_additional * additional_rate
        )
        
        # Only pay IWTC if family has children and meets work requirements
        return where(
            (num_children > 0) * meets_work_hours,
            iwtc_amount,
            0
        )
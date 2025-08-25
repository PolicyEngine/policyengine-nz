"""Best Start Tax Credit calculation for Working for Families."""

from policyengine_nz.model_api import *


class child_birth_date(Variable):
    value_type = str
    entity = Person
    definition_period = ETERNITY
    label = "Child birth date"
    documentation = "Date of birth for determining Best Start eligibility"
    reference = "https://www.ird.govt.nz/working-for-families/types/best-start"


class child_age_months(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR
    label = "Child age in months"
    documentation = "Age of child in months for Best Start calculations"
    reference = "https://www.ird.govt.nz/working-for-families/types/best-start"

    def formula(person, period, parameters):
        age = person("age", period)
        # Convert age in years to approximate age in months
        return age * 12


class best_start(Variable):
    value_type = float
    entity = Family
    definition_period = YEAR
    label = "Best Start Tax Credit"
    documentation = "Annual Best Start Tax Credit payment for young children"
    reference = "https://www.ird.govt.nz/working-for-families/types/best-start"
    unit = NZD

    def formula(family, period, parameters):
        # Get parameters
        p = parameters(period).gov.ird.working_for_families.best_start

        # Count eligible children (born after cutoff, under max age)
        children_ages_months = family.members("child_age_months", period)
        is_child = family.members("is_child", period)

        # Check age eligibility (under 3 years = 36 months)
        max_age_months = p.eligibility.max_age_months
        eligible_by_age = children_ages_months <= max_age_months

        # For now, assume all children born after cutoff date are eligible
        # In a full implementation, would check actual birth dates
        eligible_children = family.sum(is_child * eligible_by_age)

        # Get family income and Best Start parameters
        family_income = family("family_income", period)
        weekly_rate = p.rates.weekly_rate
        annual_rate = weekly_rate * WEEKS_IN_YEAR

        # Calculate base Best Start amount
        base_amount = eligible_children * annual_rate

        # Apply income test for children in years 2 and 3
        # For simplicity, applying composite income test
        # In full implementation, would track each child's age precisely
        income_threshold = p.income_test.years_2_3_threshold
        abatement_rate = p.income_test.abatement_rate

        # Calculate reduction for income above threshold
        excess_income = max_(0, family_income - income_threshold)
        reduction = excess_income * abatement_rate

        # Apply reduction (but not below zero)
        final_amount = max_(0, base_amount - reduction)

        return where(eligible_children > 0, final_amount, 0)

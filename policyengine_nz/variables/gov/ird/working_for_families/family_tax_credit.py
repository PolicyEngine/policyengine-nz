"""Family Tax Credit calculation for Working for Families."""

from policyengine_nz.model_api import *


class family_tax_credit(Variable):
    value_type = float
    entity = Family
    definition_period = YEAR
    label = "Family Tax Credit"
    documentation = (
        "Annual Family Tax Credit payment under Working for Families"
    )
    reference = (
        "https://www.ird.govt.nz/working-for-families/types/family-tax-credit"
    )
    unit = NZD

    def formula(family, period, parameters):
        # Get family parameters
        family_income = family("family_income", period)
        num_children = family("num_children", period)

        # Get children by age groups
        children_0_15 = family.sum(
            family.members("age", period)
            <= 15 * family.members("is_child", period)
        )
        children_16_18 = family.sum(
            (family.members("age", period) >= 16)
            * (family.members("age", period) <= 18)
            * family.members("is_child", period)
        )

        # Get parameters
        p = parameters(
            period
        ).gov.ird.working_for_families.family_tax_credit_rates.rates
        income_test = parameters(
            period
        ).gov.ird.working_for_families.family_tax_credit_income_test.thresholds

        # Calculate base FTC entitlement
        ftc_base = (
            children_0_15 * p.child_0_15 + children_16_18 * p.child_16_18
        )

        # Apply income test
        full_payment_threshold = income_test.full_payment_threshold
        abatement_rate = income_test.abatement_rate

        # Calculate reduction for income above threshold
        excess_income = max_(0, family_income - full_payment_threshold)
        reduction = excess_income * abatement_rate

        # Calculate final FTC (cannot be negative)
        ftc_final = max_(0, ftc_base - reduction)

        return where(num_children > 0, ftc_final, 0)

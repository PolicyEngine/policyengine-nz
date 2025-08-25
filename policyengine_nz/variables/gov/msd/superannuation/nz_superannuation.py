"""New Zealand Superannuation payment calculation."""

from policyengine_nz.model_api import *


class receiving_nz_super(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Receiving NZ Superannuation"
    documentation = "Whether person is receiving New Zealand Superannuation"
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/nz-superannuation.html"


class living_alone(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Living alone"
    documentation = (
        "Whether person is living alone for superannuation rate purposes"
    )


class nz_superannuation(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "New Zealand Superannuation"
    documentation = "Annual New Zealand Superannuation payment"
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/nz-superannuation.html"
    unit = NZD

    def formula(person, period, parameters):
        # Check basic eligibility
        receiving_super = person("receiving_nz_super", period)
        age = person("age", period)
        has_partner = person("has_partner", period)
        living_alone = person("living_alone", period)

        # Get parameters
        p = parameters(period).gov.msd.superannuation.payment_rates
        eligibility = p.eligibility
        rates = p.rates

        # Check age eligibility
        eligible_by_age = age >= eligibility.age_threshold

        # Determine rate based on living arrangements
        rate_weekly = select(
            [
                not_(has_partner) * living_alone,  # Single living alone
                not_(has_partner)
                * not_(living_alone),  # Single sharing accommodation
                has_partner,  # Married/partnered
            ],
            [
                rates.single_living_alone,
                rates.single_sharing,
                rates.couple_each,
            ],
            default=0,
        )

        # Convert to annual amount
        annual_amount = rate_weekly * WEEKS_IN_YEAR

        # Apply eligibility conditions
        eligible = receiving_super * eligible_by_age

        return where(eligible, annual_amount, 0)

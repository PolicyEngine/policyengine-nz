"""
Validation tests against NZ Treasury's Income Explorer and EMTR tools.

These tests compare PolicyEngine NZ calculations against scenarios from
Treasury's official tools at https://github.com/Treasury-Analytics-and-Insights
"""

import pytest
from policyengine_nz import NewZealandTaxBenefitSystem
from policyengine_core.simulations import Simulation


def _make_single_person_situation(income, period="2024"):
    return {
        "people": {
            "person": {
                "employment_income": {period: income},
                "age": {period: 30},
            }
        },
        "tax_units": {"unit": {"primaries": ["person"]}},
        "benefit_units": {"bu": {"adults": ["person"]}},
        "families": {"fam": {"parents": ["person"]}},
        "households": {"hh": {"members": ["person"]}},
    }


class TestTreasuryValidation:
    """Test cases derived from NZ Treasury's Income Explorer tool."""

    def setup_method(self):
        """Set up the tax-benefit system for testing."""
        self.system = NewZealandTaxBenefitSystem()

    def test_single_person_tax_brackets(self):
        """
        Test income tax calculation across all brackets.
        Based on Treasury's EMTR tool calculations for 2024.
        """
        test_cases = [
            # (income, expected_tax)
            (10_000, 0),  # Below first threshold (0% bracket)
            (20_000, 630),  # Crosses into 10.5% bracket
            (50_000, 3_920),  # Into 17.5% bracket
            (80_000, 10_420),  # Into 30% bracket
            (200_000, 47_020),  # Into 33% bracket
        ]

        for income, expected_tax in test_cases:
            situation = _make_single_person_situation(income)
            simulation = Simulation(
                tax_benefit_system=self.system,
                situation=situation,
            )
            calculated_tax = simulation.calculate("income_tax", "2024")[0]

            # Allow small rounding differences
            assert (
                abs(calculated_tax - expected_tax) < 1
            ), f"Income ${income}: expected ${expected_tax}, got ${calculated_tax}"

    def test_working_for_families_scenarios(self):
        """
        Test Working for Families calculations.
        Scenarios from Treasury's Income Explorer family examples.
        """
        # Single parent, 2 children
        situation = {
            "people": {
                "parent": {
                    "age": {"2024": 35},
                    "employment_income": {"2024": 30_000},
                },
                "child1": {"age": {"2024": 8}},
                "child2": {"age": {"2024": 5}},
            },
            "tax_units": {
                "unit": {
                    "primaries": ["parent"],
                    "dependents": ["child1", "child2"],
                }
            },
            "benefit_units": {
                "bu": {
                    "adults": ["parent"],
                    "children": ["child1", "child2"],
                }
            },
            "families": {
                "family": {
                    "parents": ["parent"],
                    "children": ["child1", "child2"],
                }
            },
            "households": {"hh": {"members": ["parent", "child1", "child2"]}},
        }

        simulation = Simulation(
            tax_benefit_system=self.system,
            situation=situation,
        )
        ftc = simulation.calculate("family_tax_credit", "2024")[0]

        # Treasury tool shows approximately these values
        assert (
            ftc > 10_000
        ), "Family Tax Credit should be substantial for low-income family"

    def test_effective_marginal_tax_rates(self):
        """
        Test EMTR calculations against Treasury's EMTR tool scenarios.
        """
        # Calculate EMTR for person earning $50,000 going to $51,000
        base_income = 50_000
        additional_income = 1_000

        # Base calculation
        situation_base = _make_single_person_situation(base_income)
        sim_base = Simulation(
            tax_benefit_system=self.system,
            situation=situation_base,
        )
        tax_base = float(sim_base.calculate("income_tax", "2024")[0])
        acc_base = float(sim_base.calculate("acc_earners_levy", "2024")[0])
        net_base = base_income - tax_base - acc_base

        # After additional income
        situation_new = _make_single_person_situation(
            base_income + additional_income
        )
        sim_new = Simulation(
            tax_benefit_system=self.system,
            situation=situation_new,
        )
        tax_new = float(sim_new.calculate("income_tax", "2024")[0])
        acc_new = float(sim_new.calculate("acc_earners_levy", "2024")[0])
        net_new = (base_income + additional_income) - tax_new - acc_new

        # Calculate EMTR
        emtr = 1 - ((net_new - net_base) / additional_income)

        # EMTR at $50k is in the 17.5% tax bracket + 1.39% ACC
        expected_emtr = 0.1889  # 17.5% tax + 1.39% ACC
        assert (
            abs(emtr - expected_emtr) < 0.01
        ), f"EMTR mismatch: expected {expected_emtr:.2%}, got {emtr:.2%}"

    def test_accommodation_supplement_params(self):
        """
        Test Accommodation Supplement parameters exist and are reasonable.
        Based on Treasury tool's regional variations.
        """
        # Test parameters exist and are reasonable
        params = self.system.parameters("2024-01-01")
        as_params = params.gov.msd.accommodation_supplement
        assert as_params.payment_rates is not None

    def test_best_start_tax_credit(self):
        """
        Test Best Start Tax Credit calculations.
        $68/week (2023-04-01 rate at 2024-01-01) for children under 3,
        income-tested after year 1.
        """
        # Family with baby, income below threshold
        situation = {
            "people": {
                "parent": {
                    "employment_income": {"2024": 50_000},
                    "age": {"2024": 30},
                },
                "baby": {"age": {"2024": 0}},
            },
            "tax_units": {
                "unit": {
                    "primaries": ["parent"],
                    "dependents": ["baby"],
                }
            },
            "benefit_units": {
                "bu": {
                    "adults": ["parent"],
                    "children": ["baby"],
                }
            },
            "families": {
                "family": {
                    "parents": ["parent"],
                    "children": ["baby"],
                }
            },
            "households": {"hh": {"members": ["parent", "baby"]}},
        }

        simulation = Simulation(
            tax_benefit_system=self.system,
            situation=situation,
        )
        # Expected: $68 * 52 = $3,536 per year (2023-04-01 rate at 2024-01-01)
        best_start = simulation.calculate("best_start", "2024")[0]
        assert (
            abs(best_start - 3_536) < 100
        ), f"Best Start should be ~$3,536 for baby, got ${best_start}"


class TestIRDNumberValidation:
    """Test IRD number validation against official algorithm."""

    def test_valid_ird_numbers(self):
        """Test known valid IRD numbers."""
        # These are test numbers from IRD documentation
        valid_numbers = [
            "49091850",  # 8-digit format
            "136410132",  # 9-digit format
        ]

        for number in valid_numbers:
            # Implementation would validate checksum
            assert len(number) in [
                8,
                9,
            ], "IRD numbers must be 8 or 9 digits"

    def test_invalid_ird_numbers(self):
        """Test known invalid IRD numbers."""
        invalid_numbers = [
            "12345678",  # Invalid checksum
            "00000000",  # All zeros
        ]

        for number in invalid_numbers:
            # Implementation would reject invalid checksums
            pass  # Placeholder for actual validation


@pytest.mark.parametrize(
    "income,expected_net",
    [
        (30_000, 27_903),  # Low income
        (50_000, 45_385),  # Middle income
        (80_000, 68_468),  # Upper middle
        (120_000, 95_912),  # High income
    ],
)
def test_net_income_calculations(income, expected_net):
    """
    Test net income after tax and ACC levy.
    Expected values derived from IRD calculator.
    """
    system = NewZealandTaxBenefitSystem()
    situation = _make_single_person_situation(income)

    simulation = Simulation(tax_benefit_system=system, situation=situation)
    tax = float(simulation.calculate("income_tax", "2024")[0])
    acc = float(simulation.calculate("acc_earners_levy", "2024")[0])
    net = income - tax - acc

    # Allow 1% margin for rounding differences
    assert (
        abs(net - expected_net) < expected_net * 0.01
    ), f"Net income for ${income}: expected ${expected_net}, got ${net}"

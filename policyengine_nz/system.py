"""
New Zealand tax and benefit system implementation.

This module defines the main tax-benefit system class that loads all
parameters and variables for New Zealand's social and fiscal policies.
"""

from policyengine_core.taxbenefitsystems import TaxBenefitSystem
from policyengine_nz.entities import entities
from pathlib import Path
import os


COUNTRY_DIR = Path(__file__).parent


class NewZealandTaxBenefitSystem(TaxBenefitSystem):
    """
    The New Zealand tax and benefit system.
    
    This class represents the complete New Zealand tax and benefit system,
    including income tax, GST, ACC, Working for Families, benefits,
    and other social assistance programs.
    """
    
    entities = entities
    # parameters_dir = COUNTRY_DIR / "parameters"  # Temporarily disabled
    variables_dir = COUNTRY_DIR / "variables"
    auto_carry_over_input_variables = True
    basic_inputs = [
        "age",
        "employment_income", 
        "self_employment_income",
        "investment_income",
        "rental_income",
        "benefit_income",
        "is_disabled",
        "is_carer",
        "is_student",
        "rent",
        "region",
        "accommodation_costs",
    ]
    
    def __init__(self, reform=None):
        """
        Initialize the New Zealand tax-benefit system.
        
        Args:
            reform: Optional reform to apply to the baseline system
        """
        # Initialize without parameters first to test basic system
        from policyengine_core.taxbenefitsystems import TaxBenefitSystem
        TaxBenefitSystem.__init__(self, entities)
        
        # Apply reform if provided
        if reform is not None:
            self.apply_reform(reform)
    
    # Entity properties are handled by parent class


# Alias for consistency with other PolicyEngine countries
CountryTaxBenefitSystem = NewZealandTaxBenefitSystem
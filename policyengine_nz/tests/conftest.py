"""
Pytest configuration for PolicyEngine New Zealand tests.

This file configures pytest to discover and run YAML-based policy tests.
"""

import pytest
import yaml
from pathlib import Path
from policyengine_nz import NewZealandTaxBenefitSystem
from policyengine_core.simulations import Simulation


def pytest_collect_file(parent, path):
    """Custom collector for YAML test files."""
    if path.ext == ".yaml" and path.basename.startswith("test_"):
        return YamlFile.from_parent(parent, fspath=path)


class YamlFile(pytest.File):
    """Custom file collector for YAML tests."""
    
    def collect(self):
        """Collect test items from YAML file."""
        with open(self.fspath) as f:
            test_cases = yaml.safe_load(f)
            
        for i, test_case in enumerate(test_cases):
            name = test_case.get("name", f"test_{i}")
            yield YamlTestItem.from_parent(
                self, 
                name=name,
                spec=test_case
            )


class YamlTestItem(pytest.Item):
    """Custom test item for YAML test cases."""
    
    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec
    
    def runtest(self):
        """Run the YAML test case."""
        system = NewZealandTaxBenefitSystem()
        
        # Build situation from input
        situation = self.spec.get("input", {})
        period = str(self.spec.get("period", "2024"))
        
        # Create simulation
        simulation = Simulation(
            tax_benefit_system=system,
            situation=situation
        )
        
        # Check outputs
        expected_outputs = self.spec.get("output", {})
        for variable_name, expected_value in expected_outputs.items():
            if isinstance(expected_value, dict):
                # Handle per-entity outputs
                for entity_name, entity_expected in expected_value.items():
                    calculated = simulation.calculate(variable_name, period)
                    # Would need entity index mapping here
                    pass
            else:
                # Simple case: single value
                calculated = simulation.calculate(variable_name, period)
                if hasattr(calculated, "__len__"):
                    calculated = calculated[0]
                
                # Allow small tolerance for floating point comparisons
                if isinstance(expected_value, (int, float)):
                    assert abs(calculated - expected_value) < 0.01, \
                        f"{variable_name}: expected {expected_value}, got {calculated}"
                else:
                    assert calculated == expected_value, \
                        f"{variable_name}: expected {expected_value}, got {calculated}"
    
    def reportinfo(self):
        """Report test location."""
        return self.fspath, 0, f"[{self.name}]"
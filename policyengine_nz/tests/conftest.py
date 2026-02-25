import pytest
from policyengine_nz.system import NewZealandTaxBenefitSystem
from policyengine_core.tools.test_runner import OpenFiscaPlugin


def pytest_configure(config):
    tax_benefit_system = NewZealandTaxBenefitSystem()
    config.pluginmanager.register(
        OpenFiscaPlugin(tax_benefit_system, options={}),
        name="openfisca",
    )

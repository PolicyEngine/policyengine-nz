# PolicyEngine New Zealand

[![Test](https://github.com/PolicyEngine/policyengine-nz/actions/workflows/test.yml/badge.svg)](https://github.com/PolicyEngine/policyengine-nz/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/policyengine-nz.svg)](https://badge.fury.io/py/policyengine-nz)
[![Python versions](https://img.shields.io/pypi/pyversions/policyengine-nz.svg)](https://pypi.org/project/policyengine-nz/)

PolicyEngine New Zealand is a microsimulation model for New Zealand's tax and benefit system. It enables users to calculate the effects of taxes and benefits on households, and to simulate the impacts of policy reforms.

## Features

- **Comprehensive tax system**: Income tax, ACC levies, GST
- **Working for Families**: Family Tax Credit, In-Work Tax Credit, Best Start
- **Social security benefits**: Jobseeker Support, NZ Superannuation, Sole Parent Support
- **Additional support**: Accommodation Supplement, Winter Energy Payment
- **Retirement savings**: KiwiSaver contributions and government support

## Quick Start

```bash
pip install policyengine-nz
```

```python
from policyengine_nz import NewZealandTaxBenefitSystem
from policyengine_core import Simulation

# Create system
system = NewZealandTaxBenefitSystem()

# Define a household
situation = {
    "people": {
        "person": {
            "employment_income": {"2025": 50000},
            "age": {"2025": 30}
        }
    }
}

# Run simulation
sim = Simulation(situation=situation, tax_benefit_system=system)
income_tax = sim.calculate("income_tax", "2025")
acc_levy = sim.calculate("acc_earners_levy", "2025")

print(f"Income tax: ${income_tax[0]:,.2f}")
print(f"ACC levy: ${acc_levy[0]:,.2f}")
```

## System Coverage

### Tax System (Inland Revenue Department)
- **Personal Income Tax**: Progressive rates (10.5%, 17.5%, 30%, 33%, 39%) with current thresholds
- **ACC Earner's Levy**: 1.67% on employment income up to $154,548 (2025)
- **GST**: 15% goods and services tax

### Working for Families (Inland Revenue Department)
- **Family Tax Credit**: Up to $6,552 per child aged 0-15, $8,372 per child aged 16-18
- **In-Work Tax Credit**: $5,304 base rate (2025) for working families
- **Best Start**: $73 per week for children under 3 (income-tested after first year)

### Social Security Benefits (Work and Income)
- **Jobseeker Support**: Up to $374.66 per week for single adults 25+ (2025)
- **New Zealand Superannuation**: Universal pension from age 65
- **Sole Parent Support**: Support for single parents
- **Supported Living Payment**: For people with disabilities
- **Accommodation Supplement**: Housing cost assistance (regional variations)
- **Winter Energy Payment**: Seasonal heating cost support

### Retirement Savings
- **KiwiSaver**: Auto-enrolment scheme with 3% minimum contributions and government co-contribution

## Data Sources

All parameters are sourced from official New Zealand government websites:
- [Inland Revenue Department (IRD)](https://www.ird.govt.nz/)
- [Work and Income](https://www.workandincome.govt.nz/)
- [Ministry of Social Development](https://www.msd.govt.nz/)
- [New Zealand Treasury](https://www.treasury.govt.nz/)

## Development

```bash
git clone https://github.com/PolicyEngine/policyengine-nz.git
cd policyengine-nz
make install
make test
```

## Documentation

Full documentation is available at [policyengine.org/nz/api](https://policyengine.org/nz/api)

## Contributing

We welcome contributions! Please see our [developer guide](https://policyengine.org/nz/api/developer-guide) for more information.

## License

PolicyEngine New Zealand is licensed under the [AGPL-3.0 License](LICENSE).

## Acknowledgments

This project builds on the work of New Zealand Treasury's TAWA microsimulation model and other open source tax-benefit modeling efforts. We acknowledge the valuable research and data provided by:

- New Zealand Treasury Analytics & Insights team
- Statistics New Zealand
- Parliamentary Budget Office research
- Academic researchers in tax and social policy

Special thanks to the broader PolicyEngine community and OpenFisca ecosystem for providing the technical foundation for this work.
# PolicyEngine New Zealand

PolicyEngine New Zealand is a microsimulation model for New Zealand's tax and benefit system. It enables users to calculate the effects of taxes and benefits on households, and to simulate the impacts of policy reforms.

## Features

- **Comprehensive tax system modeling**: Income tax, ACC levies, GST
- **Working for Families**: Family Tax Credit, In-Work Tax Credit, Best Start
- **Social security benefits**: Jobseeker Support, New Zealand Superannuation, Sole Parent Support, Supported Living Payment
- **Additional support**: Accommodation Supplement, Winter Energy Payment
- **Retirement savings**: KiwiSaver contributions and government support

## Key Components

### Tax System
- Personal income tax with progressive brackets (10.5%, 17.5%, 30%, 33%, 39%)
- ACC Earner's Levy (1.67% on employment income up to cap)
- Goods and Services Tax (GST) at 15%

### Benefits and Tax Credits  
- **Working for Families**: Comprehensive family support system including Family Tax Credit, In-Work Tax Credit, and Best Start payments for young children
- **Social Security**: Jobseeker Support, New Zealand Superannuation (universal pension), and targeted support for sole parents and people with disabilities
- **Housing Support**: Accommodation Supplement to help with housing costs

### Retirement Savings
- **KiwiSaver**: Auto-enrolment retirement savings scheme with employer and government contributions

## Getting Started

```bash
pip install policyengine-nz
```

```python
from policyengine_nz import NewZealandTaxBenefitSystem

# Create a tax and benefit system
system = NewZealandTaxBenefitSystem()

# Define a situation
situation = {
    "people": {
        "person": {
            "employment_income": {"2025": 50000},
            "age": {"2025": 30}
        }
    }
}

# Calculate income tax
from policyengine_core import Simulation
sim = Simulation(situation=situation, tax_benefit_system=system)
income_tax = sim.calculate("income_tax", "2025")
print(f"Income tax: ${income_tax[0]:,.2f}")
```

## Official Data Sources

This model is built using official New Zealand government sources:
- [Inland Revenue Department (IRD)](https://www.ird.govt.nz/) - Tax rates, Working for Families, KiwiSaver
- [Work and Income](https://www.workandincome.govt.nz/) - Benefit rates and eligibility  
- [Ministry of Social Development](https://www.msd.govt.nz/) - Social policy framework
- [New Zealand Treasury](https://www.treasury.govt.nz/) - Economic modeling and analysis

## Contributing

We welcome contributions! Please see our [developer guide](developer-guide.md) for information on how to contribute to PolicyEngine New Zealand.

## License

PolicyEngine New Zealand is released under the [AGPL-3.0 License](https://github.com/PolicyEngine/policyengine-nz/blob/main/LICENSE).
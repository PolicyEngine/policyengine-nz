# Installation

## Requirements

- Python 3.10 or higher
- pip or uv package manager

## Install from PyPI

```bash
pip install policyengine-nz
```

## Install from source

For development or to get the latest changes:

```bash
git clone https://github.com/PolicyEngine/policyengine-nz.git
cd policyengine-nz
pip install -e ".[dev]"
```

## Using uv (recommended for development)

```bash
git clone https://github.com/PolicyEngine/policyengine-nz.git
cd policyengine-nz
uv sync --dev
```

## Verify installation

Test that the installation works:

```python
import policyengine_nz
from policyengine_nz import NewZealandTaxBenefitSystem

# Create system
system = NewZealandTaxBenefitSystem()
print("PolicyEngine New Zealand installed successfully!")
```

## Development setup

For developers working on PolicyEngine New Zealand:

```bash
# Clone repository
git clone https://github.com/PolicyEngine/policyengine-nz.git
cd policyengine-nz

# Install with development dependencies
uv sync --dev

# Run tests to verify setup
uv run pytest

# Run policy tests
uv run python -m policyengine_test policyengine_nz/tests/policy --country_package policyengine_nz

# Format code
uv run black . -l 79
```
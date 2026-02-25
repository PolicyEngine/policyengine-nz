# PolicyEngine New Zealand Makefile

.PHONY: help install test format lint clean docs build changelog

help:  ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package and dependencies
	uv sync --dev

test:  ## Run all tests
	uv run pytest -xvs
	uv run python -m policyengine_test policyengine_nz/tests/policy --country_package policyengine_nz

format:  ## Format code with Black
	uv run black . -l 79

lint:  ## Check code formatting
	uv run black . --check -l 79

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:  ## Build documentation
	cd docs && myst build

build:  ## Build package
	uv build

changelog:  ## Update changelog
	python .github/bump_version.py
	towncrier build --yes --version $$(python -c "import re; print(re.search(r'version = \"(.+?)\"', open('pyproject.toml').read()).group(1))")

release:  ## Prepare release
	@echo "Preparing release..."
	$(MAKE) format
	$(MAKE) test
	$(MAKE) changelog
	@echo "Ready for release. Create and push a git tag to trigger release workflow."

debug:  ## Run debug session
	uv run python -c "from policyengine_nz import NewZealandTaxBenefitSystem; system = NewZealandTaxBenefitSystem(); print('System loaded successfully')"
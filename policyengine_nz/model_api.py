"""
Model API for PolicyEngine New Zealand.

This module exposes commonly used functions and classes for variable and parameter definitions.
"""

# Import core PolicyEngine functionality
from policyengine_core.variables import Variable
from policyengine_core.parameters import ParameterNode
from policyengine_core.periods import (
    DAY, MONTH, YEAR, ETERNITY, 
    Period, period
)
from policyengine_core.holders import set_input_divide_by_period, set_input_dispatch_by_period
from policyengine_core.enums import Enum
from policyengine_core.reforms import Reform
from policyengine_core.data_storage import in_memory_storage

# Import entities
from .entities import entities, Person, TaxUnit, BenefitUnit, Family, Household
from .typing import ArrayLike

# Mathematical operations
import numpy as np
from numpy import (
    absolute as abs_,
    ceil as ceil_,
    floor as floor_,
    maximum as max_,
    minimum as min_,
    round as round_,
    where,
    select,
    logical_not as not_,
    logical_and as and_,
    logical_or as or_,
    any as any_,
    all as all_,
)

# Currency unit
NZD = "currency-NZD"

# Common constants for New Zealand calculations
WEEKS_IN_YEAR = 52
DAYS_IN_YEAR = 365
MONTHS_IN_YEAR = 12
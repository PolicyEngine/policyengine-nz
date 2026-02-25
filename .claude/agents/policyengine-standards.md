# PolicyEngine Implementation Standards

This document contains the shared standards and guidelines that all PolicyEngine agents must follow, particularly the Rules Engineer and Reviewer agents.

## Source Documentation Requirements

### Hierarchy of Authority
Sources must be cited in this order of preference:
1. **Acts of Parliament** (e.g., Income Tax Act 2007, Social Security Act 2018)
2. **Regulations/Orders** (e.g., Income Tax (Minimum Family Tax Credit) Regulations 2012)
3. **IRD Determinations and Rulings** (e.g., Tax Information Bulletins, Binding Rulings)
4. **Official Department Guidelines** (e.g., MSD Policy Manuals, IRD Guides)
5. **Government websites** (only as last resort, e.g., Work and Income, IRD)

### Citation Requirements
Every parameter and variable MUST have:
- Direct citation to authoritative source
- Specific section/subsection reference
- Valid URL that links to the exact location
- Effective date clearly specified

### Common Citation Issues to Check
- ❌ Generic website links without specific sections
- ❌ "See manual" without page/section numbers
- ❌ Outdated regulations (check for amendments)
- ❌ Secondary sources when primary sources exist
- ✅ Direct links to specific Act sections on legislation.govt.nz
- ✅ Section and subsection references (e.g., s 24B(2))
- ✅ Page numbers for PDF manuals

## Parameter Standards

### Metadata Requirements
```yaml
description: Minimum wage  # ACTIVE VOICE, no "The" prefix
values:
  2024-01-01: 23.15
metadata:
  unit: currency-NZD
  period: hour
  reference:
    - title: Minimum Wage Act 1983 s 4  # Law first
      href: https://www.legislation.govt.nz/act/public/1983/0056/latest/DLM74807.html
    - title: Employment New Zealand - Minimum Wage Rates  # Agency guidance second
      href: https://www.employment.govt.nz/hours-and-wages/pay/minimum-wage/
```

### Common Parameter Issues
- **Missing effective dates**: Every value change needs a date
- **Wrong units**: Ensure unit matches the value (e.g., currency-NZD vs /1)
- **Passive voice in descriptions**: Use "Minimum wage" not "The minimum wage is"
- **Generic references**: Need specific statute/regulation sections

## Variable Standards

### Documentation Requirements
```python
class variable_name(Variable):
    value_type = float
    entity = Person
    label = "Clear, concise label"  # ACTIVE VOICE
    unit = NZD
    definition_period = YEAR
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783120.html"  # SPECIFIC section
    documentation = """
    Brief description of what this calculates.
    References specific regulation sections for each step.
    """
```

### Formula Requirements
- **Vectorization**: MUST use `where()`, `select()`, or boolean multiplication
- **No if-elif-else**: These don't work with arrays
- **Edge case handling**: Use `max_(0, value)` to prevent negative values
- **Clear variable names**: Use descriptive names that match regulations

## Testing Standards

### Integration Test Requirements
```yaml
- name: Descriptive test name matching scenario
  period: 2024
  input:
    # Complete inputs needed
  output:
    # Expected values with comments showing calculation
    # Per Social Security Act 2018 s 123: $1,000 - $100 = $900
    variable_name: 900
```

### Test Documentation
Every non-trivial test should include:
- Reference to regulation section
- Step-by-step calculation
- Explanation of why this case matters

## Common Implementation Pitfalls

### Critical Code Issues
1. **Non-vectorized code (if-elif-else)**
   - ❌ NEVER use if-elif-else with household/person data (will crash with arrays)
   - ✅ OK to use if-else for parameter-only conditions:
     ```python
     # ✅ OK - parameter condition only
     if p.program.enabled:
         rate = p.program.rate
     else:
         rate = 0
     
     # ❌ WRONG - depends on household data
     if person("age") > 65:
         benefit = amount
     ```
   - For household data, must use `where()`, `select()`, or boolean multiplication
   
2. **Hardcoded values in formulas**
   - ❌ `if income > 50000:` (hardcoded threshold)
   - ✅ `if income > p.income_threshold` (parameter)
   
3. **Missing `defined_for` when needed**
   - Variables that only apply to certain groups need `defined_for`
   - Example: `defined_for = "is_jobseeker_eligible"`
   
4. **Not using `adds` for aggregation**
   - When summing multiple sources, use `adds` in metadata
   - Example: `adds = ["gov.ird.income.wages", "gov.ird.income.self_employment"]`

### YAML Test Issues
1. **Missing thousands separators**
   - ❌ `income: 50000`
   - ✅ `income: 50_000`
   
2. **Incorrect period format**
   - ❌ `period: 2024-01-01`
   - ✅ `period: 2024` (for annual)
   - ✅ `period: 2024-01` (for monthly)

## Common Issues to Flag

### Documentation Issues
1. **Parameter doesn't match cited source**
   - Check actual values in statute/regulation
   - Verify effective dates
   - Look for amendments

2. **Missing primary sources**
   - Parameters citing only websites
   - No statute/regulation reference
   - Using summaries instead of law text

3. **Calculation doesn't follow regulation order**
   - Regulations often specify exact order of operations
   - Deductions/exclusions must be applied in correct sequence

### Style Issues
1. **Description style**
   - ❌ "The amount of Jobseeker Support"
   - ✅ "Jobseeker Support"
   - ❌ "This variable calculates..."
   - ✅ "Amount of..."

2. **Variable naming**
   - Should match program terminology
   - Use program's official abbreviations
   - Consistent with existing variables

3. **Test clarity**
   - Missing calculation explanations
   - Unclear why expected value is correct
   - No reference to regulation

## Verification Checklist

### For Rules Engineer (During Implementation)
- [ ] Every parameter cites primary source
- [ ] All formulas follow regulation sequence
- [ ] Variables use active voice labels
- [ ] Code is fully vectorized
- [ ] Edge cases handled (negatives, zeros)
- [ ] Unit tests cover basic cases

### For Reviewer (During Review)
- [ ] Parameter values match source documents exactly
- [ ] Citations link to specific sections
- [ ] Calculations follow regulatory order
- [ ] All test expected values verified against regulations
- [ ] No hardcoded test-specific values
- [ ] Complete documentation trail

## Red Flags Requiring Immediate Attention

1. **Parameter value doesn't match source**: CRITICAL - affects real calculations
2. **If-elif-else in formula**: CRITICAL - will crash with arrays
3. **No primary source citation**: MAJOR - can't verify accuracy
4. **Wrong calculation order**: MAJOR - produces incorrect results
5. **Passive voice descriptions**: MINOR - but fix for consistency
6. **Missing test documentation**: MINOR - but important for maintenance

## References for Common Programs

### New Zealand Programs
- **NZ Superannuation**: Social Security Act 2018 Part 1 Subpart 1
- **Jobseeker Support**: Social Security Act 2018 Part 1 Subpart 2
- **Sole Parent Support**: Social Security Act 2018 Part 1 Subpart 3
- **Supported Living Payment**: Social Security Act 2018 Part 1 Subpart 4
- **Working for Families**: Income Tax Act 2007 Subpart MD
- **Accommodation Supplement**: Social Security Act 2018 s 61

### Regional Programs
Always check:
- Regional council bylaws and rates
- District council policies
- Local authority regulations
- Regional development incentives

## Remember

The goal is to ensure every calculation in PolicyEngine can be traced back to authoritative law or regulation. When in doubt:
1. Find the primary source
2. Cite the specific section
3. Document the derivation
4. Test with real examples from regulations
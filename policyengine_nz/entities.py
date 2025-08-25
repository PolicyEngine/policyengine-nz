"""
Entity definitions for the New Zealand tax and benefit system.

References:
- Inland Revenue Department: https://www.ird.govt.nz/
- Work and Income: https://www.workandincome.govt.nz/
- Ministry of Social Development: https://www.msd.govt.nz/
- New Zealand Treasury: https://www.treasury.govt.nz/
"""

from policyengine_core.entities import build_entity


Person = build_entity(
    key="person",
    plural="people",
    label="Person",
    doc="""
    An individual person in New Zealand.
    
    This is the base entity for all individual-level calculations including
    income tax, ACC levies, and individual social security payments.
    """,
    is_person=True,
)


TaxUnit = build_entity(
    key="tax_unit",
    plural="tax_units",
    label="Tax unit",
    doc="""
    A New Zealand tax filing unit.
    
    In New Zealand, individuals generally file taxes separately, but there are
    some provisions for couples (e.g., Working for Families, KiwiSaver).
    This entity represents a tax return filing unit.
    
    Reference: https://www.ird.govt.nz/income-tax/income-tax-for-individuals
    """,
    containing_entities=["household"],
    roles=[
        {
            "key": "primary",
            "plural": "primaries",
            "label": "Primary taxpayer",
            "doc": "The primary person filing the tax return",
        },
        {
            "key": "spouse",
            "plural": "spouses",
            "label": "Spouse",
            "doc": "The spouse/partner of the primary taxpayer (if applicable)",
            "max": 1,
        },
        {
            "key": "dependent",
            "plural": "dependents",
            "label": "Dependent",
            "doc": "Dependent children or other dependents",
        },
    ],
)


BenefitUnit = build_entity(
    key="benefit_unit",
    plural="benefit_units",
    label="Benefit unit",
    doc="""
    A social security assessment unit for Work and Income payments.
    
    This represents the unit used to assess eligibility and calculate payments
    for New Zealand social security benefits. It typically includes a person,
    their partner (if applicable), and dependent children.
    
    Reference: https://www.workandincome.govt.nz/about-work-and-income/how-we-calculate-your-payments.html
    """,
    containing_entities=["household"],
    roles=[
        {
            "key": "adult",
            "plural": "adults",
            "label": "Adult",
            "doc": "Adult member of the benefit unit",
            "max": 2,
        },
        {
            "key": "child",
            "plural": "children",
            "label": "Child",
            "doc": "Dependent child in the benefit unit",
        },
    ],
)


Family = build_entity(
    key="family",
    plural="families",
    label="Family",
    doc="""
    A family unit for Working for Families and family assistance payments.
    
    Used primarily for Working for Families Tax Credits, Best Start payments, 
    and other family assistance programs. Includes parents/guardians and 
    dependent children.
    
    Reference: https://www.ird.govt.nz/working-for-families
    """,
    containing_entities=["household"],
    roles=[
        {
            "key": "parent",
            "plural": "parents",
            "label": "Parent",
            "doc": "Parent or guardian in the family",
            "max": 2,
        },
        {
            "key": "child",
            "plural": "children",
            "label": "Child",
            "doc": "Dependent child in the family",
        },
    ],
)


Household = build_entity(
    key="household",
    plural="households",
    label="Household",
    doc="""
    A physical household in New Zealand.
    
    This represents all people living at the same address, used for
    household-level calculations such as Accommodation Supplement and some
    means testing provisions.
    
    Reference: https://www.stats.govt.nz/methods/definitions-of-household-and-family
    """,
    roles=[
        {
            "key": "member",
            "plural": "members",
            "label": "Member",
            "doc": "A person living in the household",
        },
    ],
)


entities = [Person, TaxUnit, BenefitUnit, Family, Household]

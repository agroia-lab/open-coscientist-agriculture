"""Shared pytest fixtures for the coscientist test suite."""

import pytest

from coscientist.custom_types import (
    ParsedHypothesis,
    ReviewedHypothesis,
)


@pytest.fixture
def sample_hypothesis():
    """A minimal ParsedHypothesis for testing."""
    return ParsedHypothesis(
        uid="test-uid-001",
        hypothesis="Increased soil salinity reduces tomato root colonization by mycorrhizal fungi.",
        predictions=[
            "Tomato plants in high-salinity soils show 40% fewer mycorrhizal structures.",
            "Root exudate profiles shift under salinity stress.",
        ],
        assumptions=[
            "Salinity directly affects fungal hyphal growth.",
            "Mycorrhizal colonization is measurable via microscopy.",
        ],
    )


@pytest.fixture
def sample_reviewed_hypothesis():
    """A minimal ReviewedHypothesis for testing."""
    return ReviewedHypothesis(
        uid="test-uid-002",
        hypothesis="ALS-inhibiting herbicides select for resistant Phelipanche ramosa biotypes.",
        predictions=[
            "Repeated application increases frequency of resistant individuals.",
            "Cross-resistance to other ALS inhibitors is observed.",
        ],
        assumptions=[
            "Genetic variation for ALS resistance exists in P. ramosa populations.",
            "Selection pressure from herbicides is sufficient to shift allele frequencies.",
        ],
        causal_reasoning="Herbicide application creates a strong selection gradient favoring individuals with ALS mutations.",
        assumption_research_results={
            "ALS resistance exists": "Evidence found in multiple weed species.",
            "Selection pressure sufficient": "Field studies show resistance emergence within 5 generations.",
        },
        verification_result="Hypothesis is well-supported by existing literature on herbicide resistance evolution.",
    )


@pytest.fixture
def sample_reviewed_hypothesis_2():
    """A second ReviewedHypothesis for tournament testing."""
    return ReviewedHypothesis(
        uid="test-uid-003",
        hypothesis="Cover crops suppress Phelipanche germination through allelopathic compounds.",
        predictions=[
            "Brassica cover crop residues reduce Phelipanche germination by 60%.",
            "Allelopathic compounds are detectable in soil after cover crop incorporation.",
        ],
        assumptions=[
            "Brassica species produce glucosinolate breakdown products toxic to Phelipanche.",
            "Allelopathic compounds persist in soil long enough to affect germination.",
        ],
        causal_reasoning="Glucosinolate hydrolysis products inhibit Phelipanche seed germination signaling pathways.",
        assumption_research_results={
            "Glucosinolates toxic": "In vitro studies confirm toxicity at relevant concentrations.",
            "Persistence in soil": "Half-life of isothiocyanates is 3-14 days in field soil.",
        },
        verification_result="Partially supported; field validation needed for efficacy claims.",
    )


@pytest.fixture
def sample_markdown_hypothesis():
    """A raw markdown hypothesis string as returned by an LLM."""
    return """# Hypothesis
Soil microbiome diversity correlates with resistance to Phelipanche ramosa parasitism.

# Predictions
1. Fields with higher microbial diversity show lower Phelipanche infestation rates.
2. Inoculating soil with diverse microbial consortia reduces Phelipanche attachment.
3. Antibiotic-treated soils show increased susceptibility to parasitism.

# Assumptions
1. Microbial diversity can be reliably measured via 16S rRNA sequencing.
2. Some soil microbes produce compounds that inhibit Phelipanche germination stimulants.
"""

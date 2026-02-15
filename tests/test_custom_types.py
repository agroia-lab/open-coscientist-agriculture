"""Tests for coscientist/custom_types.py - Pydantic data models."""

import pytest

from coscientist.custom_types import ParsedHypothesis, ReviewedHypothesis, RankingMatchResult


class TestParsedHypothesis:
    """Tests for ParsedHypothesis model."""

    def test_auto_uuid(self):
        h = ParsedHypothesis(
            hypothesis="test",
            predictions=["p1"],
            assumptions=["a1"],
        )
        assert h.uid is not None
        assert len(h.uid) == 36  # UUID format

    def test_explicit_uid(self):
        h = ParsedHypothesis(
            uid="custom-id",
            hypothesis="test",
            predictions=["p1"],
            assumptions=["a1"],
        )
        assert h.uid == "custom-id"

    def test_parent_uid_default_none(self):
        h = ParsedHypothesis(
            hypothesis="test",
            predictions=["p1"],
            assumptions=["a1"],
        )
        assert h.parent_uid is None

    def test_parent_uid_set(self):
        h = ParsedHypothesis(
            hypothesis="test",
            predictions=["p1"],
            assumptions=["a1"],
            parent_uid="parent-123",
        )
        assert h.parent_uid == "parent-123"

    def test_model_dump_roundtrip(self):
        h = ParsedHypothesis(
            uid="roundtrip-id",
            hypothesis="My hypothesis",
            predictions=["p1", "p2"],
            assumptions=["a1"],
            parent_uid="parent-id",
        )
        data = h.model_dump()
        h2 = ParsedHypothesis(**data)
        assert h == h2


class TestReviewedHypothesis:
    """Tests for ReviewedHypothesis model."""

    def test_inherits_parsed(self, sample_reviewed_hypothesis):
        assert hasattr(sample_reviewed_hypothesis, "hypothesis")
        assert hasattr(sample_reviewed_hypothesis, "predictions")
        assert hasattr(sample_reviewed_hypothesis, "assumptions")
        assert hasattr(sample_reviewed_hypothesis, "causal_reasoning")
        assert hasattr(sample_reviewed_hypothesis, "verification_result")

    def test_model_dump_roundtrip(self, sample_reviewed_hypothesis):
        data = sample_reviewed_hypothesis.model_dump()
        h2 = ReviewedHypothesis(**data)
        assert h2.uid == sample_reviewed_hypothesis.uid
        assert h2.causal_reasoning == sample_reviewed_hypothesis.causal_reasoning

    def test_assumption_research_results(self, sample_reviewed_hypothesis):
        assert isinstance(sample_reviewed_hypothesis.assumption_research_results, dict)
        assert len(sample_reviewed_hypothesis.assumption_research_results) > 0


class TestRankingMatchResult:
    """Tests for RankingMatchResult model."""

    def test_basic_creation(self):
        r = RankingMatchResult(
            uid1="a",
            uid2="b",
            winner=1,
            debate="Hypothesis A won because...",
        )
        assert r.uid1 == "a"
        assert r.winner == 1

    def test_model_dump_roundtrip(self):
        r = RankingMatchResult(
            uid1="x",
            uid2="y",
            winner=2,
            debate="Debate text",
        )
        data = r.model_dump()
        r2 = RankingMatchResult(**data)
        assert r == r2

"""Tests for coscientist/common.py - parsing and prompt loading."""

import pytest

from coscientist.common import (
    _parse_numbered_list,
    load_prompt,
    parse_hypothesis_markdown,
)


class TestParseHypothesisMarkdown:
    """Tests for parse_hypothesis_markdown()."""

    def test_basic_parsing(self, sample_markdown_hypothesis):
        result = parse_hypothesis_markdown(sample_markdown_hypothesis)
        assert result.hypothesis.startswith("Soil microbiome diversity")
        assert len(result.predictions) == 3
        assert len(result.assumptions) == 2
        assert result.uid  # UUID should be auto-generated

    def test_parsing_with_final_report_prefix(self):
        md = """Some preamble text
#FINAL REPORT#
# Hypothesis
Test hypothesis statement.

# Predictions
1. Prediction one.

# Assumptions
1. Assumption one.
"""
        result = parse_hypothesis_markdown(md)
        assert result.hypothesis == "Test hypothesis statement."
        assert result.predictions == ["Prediction one."]
        assert result.assumptions == ["Assumption one."]

    def test_missing_hypothesis_raises(self):
        md = """# Predictions
1. Something.

# Assumptions
1. Something else.
"""
        with pytest.raises(AssertionError, match="Hypothesis section is required"):
            parse_hypothesis_markdown(md)

    def test_missing_predictions_raises(self):
        md = """# Hypothesis
A hypothesis.

# Assumptions
1. An assumption.
"""
        with pytest.raises(AssertionError, match="Predictions section is required"):
            parse_hypothesis_markdown(md)

    def test_missing_assumptions_raises(self):
        md = """# Hypothesis
A hypothesis.

# Predictions
1. A prediction.
"""
        with pytest.raises(AssertionError, match="Assumptions section is required"):
            parse_hypothesis_markdown(md)

    def test_case_insensitive_headings(self):
        md = """# HYPOTHESIS
My hypothesis.

# PREDICTIONS
1. Prediction A.

# ASSUMPTIONS
1. Assumption A.
"""
        result = parse_hypothesis_markdown(md)
        assert result.hypothesis == "My hypothesis."
        assert result.predictions == ["Prediction A."]
        assert result.assumptions == ["Assumption A."]

    def test_multiline_predictions(self):
        md = """# Hypothesis
A test hypothesis.

# Predictions
1. First prediction that spans
   multiple lines.
2. Second prediction.

# Assumptions
1. One assumption.
"""
        result = parse_hypothesis_markdown(md)
        assert len(result.predictions) == 2
        assert "multiple lines" in result.predictions[0]


class TestParseNumberedList:
    """Tests for _parse_numbered_list()."""

    def test_basic_numbered_list(self):
        content = "1. First item\n2. Second item\n3. Third item"
        result = _parse_numbered_list(content)
        assert result == ["First item", "Second item", "Third item"]

    def test_parenthesis_format(self):
        content = "1) First\n2) Second"
        result = _parse_numbered_list(content)
        assert result == ["First", "Second"]

    def test_dash_format(self):
        content = "1- First\n2- Second"
        result = _parse_numbered_list(content)
        assert result == ["First", "Second"]

    def test_empty_content(self):
        result = _parse_numbered_list("")
        assert result == []

    def test_whitespace_only(self):
        result = _parse_numbered_list("   \n  \n  ")
        assert result == []

    def test_multiline_items(self):
        content = "1. First item that continues\n   on the next line\n2. Second item"
        result = _parse_numbered_list(content)
        assert len(result) == 2
        assert "continues" in result[0] and "next line" in result[0]

    def test_no_numbering(self):
        content = "Just a plain text line"
        result = _parse_numbered_list(content)
        assert result == ["Just a plain text line"]


class TestLoadPrompt:
    """Tests for load_prompt()."""

    def test_load_existing_prompt(self):
        prompt = load_prompt("topic_decomposition", goal="test goal", max_subtopics=3)
        assert "test goal" in prompt
        assert isinstance(prompt, str)
        assert len(prompt) > 50

    def test_load_nonexistent_prompt_raises(self):
        with pytest.raises(Exception):
            load_prompt("nonexistent_prompt_name")

    def test_prompt_renders_variables(self):
        prompt = load_prompt(
            "independent_generation",
            goal="test goal",
            literature_review="test review",
            field="weed science",
            reasoning_type="FIRST_PRINCIPLES",
            meta_review="",
        )
        assert "test goal" in prompt
        assert "weed science" in prompt

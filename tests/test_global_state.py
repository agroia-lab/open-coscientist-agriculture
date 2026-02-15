"""Tests for coscientist/global_state.py - state management and JSON persistence."""

import json
import os
import shutil
import tempfile

import pytest

from coscientist.custom_types import ParsedHypothesis, ReviewedHypothesis

try:
    from coscientist.global_state import CoscientistState, CoscientistStateManager

    HAS_GLOBAL_STATE = True
except (ImportError, Exception):
    HAS_GLOBAL_STATE = False

pytestmark = pytest.mark.skipif(
    not HAS_GLOBAL_STATE,
    reason="global_state dependencies not available (gpt_researcher, etc.)",
)


@pytest.fixture
def temp_output_dir(monkeypatch):
    """Create a temporary output directory and patch _OUTPUT_DIR."""
    tmpdir = tempfile.mkdtemp()
    monkeypatch.setattr("coscientist.global_state._OUTPUT_DIR", tmpdir)
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def state(temp_output_dir):
    """Create a fresh CoscientistState with a test goal."""
    return CoscientistState(goal="Test agricultural hypothesis generation")


class TestCoscientistState:
    """Tests for CoscientistState initialization and persistence."""

    def test_init_creates_directory(self, state, temp_output_dir):
        goal_hash = CoscientistState._hash_goal(
            "Test agricultural hypothesis generation"
        )
        goal_dir = os.path.join(temp_output_dir, goal_hash)
        assert os.path.exists(goal_dir)

    def test_init_writes_goal_file(self, state, temp_output_dir):
        goal_hash = CoscientistState._hash_goal(
            "Test agricultural hypothesis generation"
        )
        goal_file = os.path.join(temp_output_dir, goal_hash, "goal.txt")
        assert os.path.exists(goal_file)
        with open(goal_file) as f:
            assert f.read().strip() == "Test agricultural hypothesis generation"

    def test_duplicate_goal_raises(self, state, temp_output_dir):
        with pytest.raises(FileExistsError):
            CoscientistState(goal="Test agricultural hypothesis generation")

    def test_directory_permissions(self, state, temp_output_dir):
        goal_hash = CoscientistState._hash_goal(
            "Test agricultural hypothesis generation"
        )
        goal_dir = os.path.join(temp_output_dir, goal_hash)
        mode = oct(os.stat(goal_dir).st_mode & 0o777)
        assert mode == "0o700"

    def test_hash_goal_deterministic(self):
        h1 = CoscientistState._hash_goal("some goal")
        h2 = CoscientistState._hash_goal("some goal")
        assert h1 == h2

    def test_hash_goal_case_insensitive(self):
        h1 = CoscientistState._hash_goal("Some Goal")
        h2 = CoscientistState._hash_goal("some goal")
        assert h1 == h2

    def test_hash_goal_strips_whitespace(self):
        h1 = CoscientistState._hash_goal("  some goal  ")
        h2 = CoscientistState._hash_goal("some goal")
        assert h1 == h2

    def test_hash_goal_length(self):
        h = CoscientistState._hash_goal("any goal")
        assert len(h) == 12


class TestStatePersistence:
    """Tests for JSON save/load cycle."""

    def test_save_creates_json_file(self, state):
        filepath = state.save()
        assert filepath.endswith(".json")
        assert os.path.exists(filepath)

    def test_save_json_is_valid(self, state):
        filepath = state.save()
        with open(filepath) as f:
            data = json.load(f)
        assert data["goal"] == "Test agricultural hypothesis generation"

    def test_save_load_roundtrip(self, state):
        state.generated_hypotheses.append(
            ParsedHypothesis(
                uid="test-123",
                hypothesis="Test hypothesis",
                predictions=["p1"],
                assumptions=["a1"],
            )
        )
        filepath = state.save()
        loaded = CoscientistState.load(filepath)
        assert loaded.goal == state.goal
        assert len(loaded.generated_hypotheses) == 1
        assert loaded.generated_hypotheses[0].uid == "test-123"

    def test_save_increments_iteration(self, state):
        assert state._iteration == 0
        state.save()
        assert state._iteration == 1
        state.save()
        assert state._iteration == 2

    def test_list_checkpoints(self, state, temp_output_dir):
        state.save()
        state.save()
        checkpoints = CoscientistState.list_checkpoints(
            goal="Test agricultural hypothesis generation"
        )
        assert len(checkpoints) == 2
        # Newest first
        assert checkpoints[0] > checkpoints[1]

    def test_load_latest(self, state, temp_output_dir):
        state.save()
        state.generated_hypotheses.append(
            ParsedHypothesis(
                uid="latest-uid",
                hypothesis="Latest",
                predictions=["p"],
                assumptions=["a"],
            )
        )
        state.save()
        loaded = CoscientistState.load_latest(
            goal="Test agricultural hypothesis generation"
        )
        assert loaded is not None
        assert len(loaded.generated_hypotheses) == 1

    def test_load_latest_returns_none_when_empty(self, temp_output_dir):
        result = CoscientistState.load_latest(goal="nonexistent goal xyz")
        assert result is None

    def test_clear_goal_directory(self, state, temp_output_dir):
        state.save()
        result = CoscientistState.clear_goal_directory(
            "Test agricultural hypothesis generation"
        )
        assert "Successfully" in result

    def test_list_all_goals(self, state, temp_output_dir):
        goals = CoscientistState.list_all_goals()
        assert len(goals) == 1
        assert goals[0][0] == "Test agricultural hypothesis generation"


class TestStateWithTournament:
    """Tests for state serialization with complex objects."""

    def test_save_load_with_tournament(self, state, sample_reviewed_hypothesis):
        from coscientist.ranking_agent import EloTournament

        state.tournament = EloTournament(goal=state.goal)
        state.tournament.add_hypothesis(sample_reviewed_hypothesis)
        state.tournament.ratings[sample_reviewed_hypothesis.uid] = 1350

        filepath = state.save()
        loaded = CoscientistState.load(filepath)

        assert loaded.tournament is not None
        assert sample_reviewed_hypothesis.uid in loaded.tournament.hypotheses
        assert loaded.tournament.ratings[sample_reviewed_hypothesis.uid] == 1350

    def test_save_load_with_reviewed_hypotheses(self, state, sample_reviewed_hypothesis):
        state.reviewed_hypotheses.append(sample_reviewed_hypothesis)

        filepath = state.save()
        loaded = CoscientistState.load(filepath)

        assert len(loaded.reviewed_hypotheses) == 1
        assert loaded.reviewed_hypotheses[0].uid == sample_reviewed_hypothesis.uid
        assert (
            loaded.reviewed_hypotheses[0].causal_reasoning
            == sample_reviewed_hypothesis.causal_reasoning
        )


class TestCoscientistStateManager:
    """Tests for the state manager operations."""

    @pytest.fixture
    def manager(self, state, sample_reviewed_hypothesis):
        """Create a state manager with initialized tournament and proximity graph."""
        mgr = CoscientistStateManager(state)
        return mgr

    def test_goal_property(self, manager):
        assert manager.goal == "Test agricultural hypothesis generation"

    def test_not_started_initially(self, manager):
        assert not manager.is_started

    def test_not_finished_initially(self, manager):
        assert not manager.is_finished

    def test_total_hypotheses_initially_zero(self, manager):
        assert manager.total_hypotheses == 0

    def test_reflection_queue_empty(self, manager):
        assert manager.reflection_queue_is_empty

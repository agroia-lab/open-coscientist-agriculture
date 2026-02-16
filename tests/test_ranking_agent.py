"""Tests for coscientist/ranking_agent.py - ELO tournament and ranking logic."""

import pytest

from coscientist.custom_types import RankingMatchResult
from coscientist.ranking_agent import (
    DEFAULT_ELO,
    EloTournament,
    calculate_expected_score,
    update_elo,
)


class TestCalculateExpectedScore:
    """Tests for the ELO expected score calculation."""

    def test_equal_ratings(self):
        e1, e2 = calculate_expected_score(1200, 1200)
        assert abs(e1 - 0.5) < 1e-6
        assert abs(e2 - 0.5) < 1e-6

    def test_higher_rating_favored(self):
        e1, e2 = calculate_expected_score(1600, 1200)
        assert e1 > e2
        assert e1 > 0.5

    def test_scores_sum_to_one(self):
        e1, e2 = calculate_expected_score(1400, 1100)
        assert abs(e1 + e2 - 1.0) < 1e-6

    def test_symmetric(self):
        e1_a, e2_a = calculate_expected_score(1300, 1500)
        e1_b, e2_b = calculate_expected_score(1500, 1300)
        assert abs(e1_a - e2_b) < 1e-6
        assert abs(e2_a - e1_b) < 1e-6


class TestUpdateElo:
    """Tests for ELO rating updates."""

    def test_winner_1_gains_rating(self):
        new1, new2 = update_elo(1200, 1200, winner=1)
        assert new1 > 1200
        assert new2 < 1200

    def test_winner_2_gains_rating(self):
        new1, new2 = update_elo(1200, 1200, winner=2)
        assert new1 < 1200
        assert new2 > 1200

    def test_equal_ratings_equal_change(self):
        new1, new2 = update_elo(1200, 1200, winner=1)
        gain = new1 - 1200
        loss = 1200 - new2
        assert abs(gain - loss) < 1e-6

    def test_upset_win_larger_change(self):
        # Underdog (1000) beats favorite (1400)
        new1_upset, new2_upset = update_elo(1000, 1400, winner=1)
        # Expected win (1400 beats 1000)
        new1_expected, new2_expected = update_elo(1400, 1000, winner=1)

        upset_gain = new1_upset - 1000
        expected_gain = new1_expected - 1400
        assert upset_gain > expected_gain  # Underdog gains more

    def test_invalid_winner_raises(self):
        with pytest.raises(ValueError, match="Winner must be 1 or 2"):
            update_elo(1200, 1200, winner=3)

    def test_rating_conservation(self):
        r1, r2 = 1300, 1100
        new1, new2 = update_elo(r1, r2, winner=1)
        # Total rating should be conserved
        assert abs((new1 + new2) - (r1 + r2)) < 1e-6


class TestEloTournament:
    """Tests for the EloTournament class."""

    def test_add_hypothesis(self, sample_reviewed_hypothesis):
        t = EloTournament(goal="test")
        t.add_hypothesis(sample_reviewed_hypothesis)
        assert sample_reviewed_hypothesis.uid in t.hypotheses
        assert t.ratings[sample_reviewed_hypothesis.uid] == DEFAULT_ELO

    def test_add_duplicate_raises(self, sample_reviewed_hypothesis):
        t = EloTournament(goal="test")
        t.add_hypothesis(sample_reviewed_hypothesis)
        with pytest.raises(ValueError, match="already exists"):
            t.add_hypothesis(sample_reviewed_hypothesis)

    def test_get_sorted_hypotheses(
        self, sample_reviewed_hypothesis, sample_reviewed_hypothesis_2
    ):
        t = EloTournament(goal="test")
        t.add_hypothesis(sample_reviewed_hypothesis)
        t.add_hypothesis(sample_reviewed_hypothesis_2)
        # Manually adjust ratings
        t.ratings[sample_reviewed_hypothesis.uid] = 1400
        t.ratings[sample_reviewed_hypothesis_2.uid] = 1100
        sorted_h = t.get_sorted_hypotheses()
        assert sorted_h[0][0] == sample_reviewed_hypothesis.uid
        assert sorted_h[0][1] == 1400

    def test_get_win_loss_records_empty(self, sample_reviewed_hypothesis):
        t = EloTournament(goal="test")
        t.add_hypothesis(sample_reviewed_hypothesis)
        records = t.get_win_loss_records()
        assert records[sample_reviewed_hypothesis.uid] == {"wins": 0, "losses": 0}

    def test_serialization_roundtrip(
        self, sample_reviewed_hypothesis, sample_reviewed_hypothesis_2
    ):
        t = EloTournament(goal="test goal")
        t.add_hypothesis(sample_reviewed_hypothesis)
        t.add_hypothesis(sample_reviewed_hypothesis_2)
        t.ratings[sample_reviewed_hypothesis.uid] = 1350
        t.ratings[sample_reviewed_hypothesis_2.uid] = 1050

        # Add a match result
        t.match_history[
            (sample_reviewed_hypothesis.uid, sample_reviewed_hypothesis_2.uid, 1)
        ] = RankingMatchResult(
            uid1=sample_reviewed_hypothesis.uid,
            uid2=sample_reviewed_hypothesis_2.uid,
            winner=1,
            debate="Test debate",
        )
        t._past_tournament_ratings = [[1350, 1050]]

        # Serialize and deserialize
        data = t.to_dict()
        t2 = EloTournament.from_dict(data)

        assert t2.goal == "test goal"
        assert len(t2.hypotheses) == 2
        assert t2.ratings[sample_reviewed_hypothesis.uid] == 1350
        assert len(t2.match_history) == 1
        assert t2._past_tournament_ratings == [[1350, 1050]]

    def test_summarize_tournament_trajectory(
        self, sample_reviewed_hypothesis, sample_reviewed_hypothesis_2
    ):
        t = EloTournament(goal="test")
        t.add_hypothesis(sample_reviewed_hypothesis)
        t.add_hypothesis(sample_reviewed_hypothesis_2)
        t.ratings[sample_reviewed_hypothesis.uid] = 1450
        t.ratings[sample_reviewed_hypothesis_2.uid] = 1100
        t._past_tournament_ratings = [[1450, 1100]]

        summary = t.summarize_tournament_trajectory()
        assert summary["total_matches_played"] == 0
        assert summary["total_rounds_played"] == 1
        assert len(summary["top_3_elo_ratings"]) == 2
        assert summary["max_elo_rating"] == [1450]

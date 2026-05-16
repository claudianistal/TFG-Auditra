"""Unit tests for AnalysisScorer module."""
import pytest
from app.analysis.scorer import AnalysisScorer


class TestAnalysisScorer:
    """Test suite for AnalysisScorer class."""

    @pytest.fixture
    def scorer(self):
        """Create a fresh scorer instance."""
        return AnalysisScorer()

    # Essential tests for calculate_score()
    def test_calculate_score_empty(self, scorer):
        """Empty factors returns 0."""
        assert scorer.calculate_score([]) == 0

    def test_calculate_score_single_factor(self, scorer):
        """Single factor returns its weight."""
        factors = [{'weight': 35}]
        assert scorer.calculate_score(factors) == 35

    def test_calculate_score_multiple_factors(self, scorer, low_risk_score_factors):
        """Multiple factors sum correctly."""
        result = scorer.calculate_score(low_risk_score_factors)
        assert result == 15

    def test_calculate_score_capped_at_100(self, scorer):
        """Score never exceeds 100."""
        factors = [{'weight': 60}, {'weight': 70}]  # Total: 130
        assert scorer.calculate_score(factors) == 100

    # Essential tests for interpret_score()
    def test_interpret_score_bajo(self, scorer):
        """Score < 30 is bajo (low)."""
        result = scorer.interpret_score(15)
        assert result['likelihood'] == 'bajo'
        assert result['color'] == 'green'

    def test_interpret_score_medio(self, scorer):
        """Score 30-59 is medio (medium)."""
        result = scorer.interpret_score(45)
        assert result['likelihood'] == 'medio'
        assert result['color'] == 'yellow'

    def test_interpret_score_alto(self, scorer):
        """Score >= 60 is alto (high)."""
        result = scorer.interpret_score(75)
        assert result['likelihood'] == 'alto'
        assert result['color'] == 'red'

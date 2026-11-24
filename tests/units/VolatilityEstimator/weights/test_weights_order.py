import numpy as np
import pytest

from src.Exposure.VolatilityEstimator import VolatilityEstimator

"""Ce test lance le même test plusieurs fois avec une paire (lam, K) différente à chaque fois.

Il s'assure que le poids le plus grand est le dernier (jour le plus récent)
et que les poids décroissent en remontant vers le passé.
"""

@pytest.mark.parametrize(
    "lam, K",
    [
        (0.95, 120),
        (0.98, 120),
        (0.5, 5),
    ],
)
def test_weights_most_recent_is_largest(lam, K):
    weights = VolatilityEstimator.weights(lam, K)
    assert weights.argmax() == K - 1        # le plus grand poids est le dernier
    assert np.all(np.diff(weights) > 0)     # strictement croissants, du plus ancien au plus récent
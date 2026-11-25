import pytest

from src.VolatilityEstimator.EwmaMaxVolatilityEstimator import EwmaMaxVolatilityEstimator

"""Ce test lance le même test plusieurs fois avec une paire (lam, K) différente à chaque fois.

Il s'assure que la somme des poids renvoyés par weights vaut 1.
"""

@pytest.mark.parametrize(
    "lam, K",
    [
        (0.95, 120),   
        (0.98, 120),  
        (0.5, 5),      
        (1.0, 10),     # cas limite : poids égaux (moyenne simple)
    ],
)
def test_weights_sum_equals_one(lam, K):
    weights = EwmaMaxVolatilityEstimator.weights(lam, K)
    assert weights.sum() == pytest.approx(1)
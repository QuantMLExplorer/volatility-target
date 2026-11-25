import numpy as np 
import pytest

from src.VolatilityEstimator.EwmaMaxVolatilityEstimator import EwmaMaxVolatilityEstimator

"""Ce test vérifie que lorsque lam = 1, tous les poids sont égaux à 1/K."""

@pytest.mark.parametrize( "K", [5, 10, 120], ) 


def test_weights_equal_when_lambda_is_one(K): 
    weights = EwmaMaxVolatilityEstimator.weights(1, K)
    expected_weights = np.full(K, 1 / K)
    np.testing.assert_allclose(weights, expected_weights)


import pytest

from src.Config.IndexParams import IndexParams

"""Ce test lance le même test plusieurs fois avec une paire de valeurs différentes à chaque fois."""
""" Il s'assure que 0 < lam_S < lam_L <= 1  """


@pytest.mark.parametrize(
    "lam_S, lam_L",
    [
        (-0.1, 0.98),   # lam_S < 0
        (0.0, 0.98),    # lam_S == 0
        (0.98, 0.98),   # lam_S == lam_L
        (0.99, 0.98),   # lam_S > lam_L
        (0.95, 1.01),   # lam_L > 1
    ],
)
def test_lambda_invalide_leve_value_error(lam_S, lam_L):
    # Tous les champs sont valides, sauf lam_S et lam_L.
    with pytest.raises(ValueError, match="lam_S < lam_L"):
        IndexParams(
            name="test",
            index_type="price_return",
            vol_target=0.12,
            lam_S=lam_S,
            lam_L=lam_L,
            K=120,
            T=5,
            LM=1.0,
            d=3,
        )

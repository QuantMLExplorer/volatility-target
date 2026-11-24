import pytest

from src.Config.IndexParams import IndexParams

"""Ce test lance le même test plusieurs fois avec une paire de valeurs différentes à chaque fois."""
""" Il s'assure que 0 < vol_target et 0 < LM   """


@pytest.mark.parametrize(
    "vol_target, LM",
    [
        (-0.1, 0.98),   # vol_target < 0
        (0.0, 0.98),    # vol_target == 0
        (2, -0.1),   # LM < 0
        (2, 0),   # LM == 0
    ],
)
def test_lambda_invalide_leve_value_error(vol_target, LM):
    # Tous les champs sont valides, sauf vol_target, LM.
    with pytest.raises(ValueError, match="vol_target et LM doivent être > 0"):
        IndexParams(
            name="test",
            index_type="price_return",
            vol_target=vol_target,
            lam_S=0.2,
            lam_L=0.8,
            K=120,
            T=5,
            LM=LM,
            d=3,
        )
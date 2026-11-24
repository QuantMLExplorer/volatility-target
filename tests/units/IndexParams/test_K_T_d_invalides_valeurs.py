import pytest

from src.Config.IndexParams import IndexParams

"""Ce test lance le même test plusieurs fois avec une paire de valeurs différentes à chaque fois."""
""" Il s'assure que K, T >= 1 et d >= 0   """


@pytest.mark.parametrize(
    "K, T,d",
    [
        (0, 2, 0),   # K == 0
        (1, 0, 1),   # T == 0
        (0, 2, -1),   # d < 0
    ],
)
def test_lambda_invalide_leve_value_error(K, T,d):
    # Tous les champs sont valides, sauf vol_target, LM.
    with pytest.raises(ValueError, match="K, T >= 1 et d >= 0"):
        IndexParams(
            name="test",
            index_type="price_return",
            vol_target=2,
            lam_S=0.2,
            lam_L=0.8,
            K=K,
            T=T,
            LM=0.8,
            d=d,
        )
import pytest

from src.Config.IndexParams import IndexParams

"""Ce test s'assure qu'un index_type différent de price_return, total_return et excess_return lève une ValueError."""

def test_index_type_inconnu_leve_value_error():
    # Tous les champs sont valides, sauf index_type.
    with pytest.raises(ValueError, match="index_type inconnu"):
        IndexParams(
            name="test",
            index_type="inconnu",
            vol_target=0.12,
            lam_S=0.95,
            lam_L=0.98,
            K=120,
            T=5,
            LM=1.0,
            d=3,
        )
    
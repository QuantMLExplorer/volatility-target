import pytest

from src.Config.IndexParams import IndexParams

"""Ce test vérifie que K, T et d doivent obligatoirement être des entiers."""

@pytest.mark.parametrize(
    "K, T, d",
    [
        (120.5, 60, 5),    # K est un float
        (120, 60.5, 5),    # T est un float
        (120, 60, 5.5),    # d est un float
        ("120", 60, 5),    # K est une str
        (120, "60", 5),    # T est une str
        (120, 60, "5"),    # d est une str
    ],
)
def test_K_T_d_types_invalides_leve_type_error(K, T, d):
    with pytest.raises(TypeError, match="K, T et d doivent être des entiers"):
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

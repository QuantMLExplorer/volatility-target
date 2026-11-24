import pytest

from src.Config.IndexParams import IndexParams

"""Ce test lance le même test plusieurs fois avec une paire (cash_rate, day_count) différente à chaque fois.

    Il s'assure qu'un price_return, qui n'utilise pas de cash, refuse un cash_rate ou un day_count renseigné.
    """


@pytest.mark.parametrize(
    "cash_rate, day_count",
    [
        ("FedFunds", 360),          # cash_rate présent
        (None, 360)    # day_count présent 
    ],
)
def test_total_return_cash_invalide_leve_value_error(cash_rate, day_count):
    # Tous les champs sont valides, sauf cash_rate et day_count.
    with pytest.raises(ValueError, match="retirez cash_rate et day_count"):
        IndexParams(
            name="test",
            index_type="price_return",
            vol_target=0.12,
            lam_S=0.95,
            lam_L=0.98,
            K=120,
            T=5,
            LM=1.0,
            d=3,
            cash_rate=cash_rate,
            day_count=day_count,
        )
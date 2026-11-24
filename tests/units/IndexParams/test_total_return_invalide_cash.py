import pytest

from src.Config.IndexParams import IndexParams

"""Ce test lance le même test plusieurs fois avec une paire (cash_rate, day_count) différente à chaque fois.

    Il s'assure qu'un total_return refuse un cash_rate absent, ainsi qu'un day_count absent ou différent de 360 et 365.
    """

@pytest.mark.parametrize(
    "cash_rate, day_count",
    [
        (None, 360),          # cash_rate absent
        ("FedFunds", 400),    # day_count ni 360 ni 365
        ("FedFunds", None),  # day_count absent 
        (None, None)         # cash_rate et day_count absent 
    ],
)
def test_total_return_cash_invalide_leve_value_error(cash_rate, day_count):
    # Tous les champs sont valides, sauf cash_rate et day_count.
    with pytest.raises(ValueError, match="exige cash_rate et day_count"):
        IndexParams(
            name="test",
            index_type="total_return",
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
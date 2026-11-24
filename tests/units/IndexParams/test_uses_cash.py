import pytest

from src.Config.IndexParams import IndexParams

"""Ce test lance le même test plusieurs fois avec un type d'indice différent à chaque fois.
    Vérifie que uses_cash vaut False pour price_return et True pour total_return et excess_return.
"""


@pytest.mark.parametrize(
    "index_type, cash_rate, day_count, expected",
    [
        ("price_return", None, None, False),
        ("total_return", "FedFunds", 360, True),
        ("excess_return", "FedFunds", 360, True),
    ],
)
def test_uses_cash_depends_on_index_type(index_type, cash_rate, day_count, expected):
    params = IndexParams(
        name="test",
        index_type=index_type,
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
    assert params.uses_cash is expected
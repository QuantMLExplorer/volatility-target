"""Fixtures partagées par tous les tests (chargées automatiquement par pytest)."""
from pathlib import Path

import pytest

from src.Config.ConfigLoader import ConfigLoader

# conftest.py est dans src/tests : parents[0] = src/tests, parents[1] = src, parents[2] = racine du projet
JSON = Path(__file__).parents[1] / "params" / "indices.json"


@pytest.fixture(scope="session")
def cfg():
    return ConfigLoader(JSON)


@pytest.fixture(scope="session")
def params(cfg):
    """Indice DI_Dev200_12_USD : lam 0.95/0.98, K=120, T=5, LM=1, d=3, cash FedFunds (base 360)."""
    return cfg.load("DI_Dev200_12_USD")

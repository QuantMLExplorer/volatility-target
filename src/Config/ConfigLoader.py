import json 
from pathlib import Path
from src.Config.Config import IndexParams

class ConfigLoader:
    """Lit le fichier JSON et fournit des objets IndexParams."""

    def __init__(self, path):
        with open(Path(path), encoding="utf-8") as f:
            self._raw = json.load(f)

    def available(self):
        return list(self._raw)

    def load(self, name: str) -> IndexParams:
        if name not in self._raw:
            raise KeyError(f"Indice '{name}' absent. Disponibles : {self.available()}")
        return IndexParams(name=name, **self._raw[name])
import json 
from pathlib import Path
from src.Config.IndexParams import IndexParams

class ConfigLoader:
    """Lit le fichier JSON de configuration et fournit des objets IndexParams."""

    def __init__(self, path):
        with open(Path(path), encoding="utf-8") as f:
            # {nom de l'indice: {paramètre: valeur}}
            self._raw = json.load(f)   # dictionnaire dont les clés sont les noms des indices et les valeurs des dictionnaires contenant les paramètres

    def available(self):
        """Renvoie la liste des noms d'indices présents dans le JSON."""
        return list(self._raw)

    def load(self, name: str) -> IndexParams:
        """Renvoie un objet IndexParams de l'indice `name` """
        if name not in self._raw:
            raise KeyError(f"Indice '{name}' absent. Disponibles : {self.available()}")
        return IndexParams(name=name, **self._raw[name])      # transforme le dictionnaire en une liste d'arguments nommés#




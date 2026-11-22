# Volatility Target

Implémentation en Python des indices **Volatility Target** décrits dans le document *Custom Volatility Target Index Series – Ground Rules* (FTSE Russell, v2.3, mars 2025).

## Principe

La stratégie maintient un niveau de risque constant. Le client fixe une volatilité cible, et l'indice ajuste chaque jour la part investie dans le sous-jacent (un indice actions), le reste étant placé au taux sans risque :

- si la volatilité du sous-jacent monte, l'exposition aux actions diminue et la part de cash augmente ;
- si elle baisse, l'inverse se produit.

Le client fixe aussi le levier maximal `LM`, qui plafonne l'exposition.

## Types d'indices

| Type | Description |
|---|---|
| `price_return` | Valeur du portefeuille si la part `E(t)` est investie dans le sous-jacent, sans rémunération du reste |
| `total_return` | La part non investie, `1 - E(t)`, est placée au taux du cash |
| `excess_return` | Mesure uniquement ce que la stratégie rapporte au-dessus du placement au taux du cash |

## Méthodologie

### Volatilité

Calculée par moyenne mobile exponentielle (EWMA) des rendements logarithmiques quotidiens, sans soustraction de la moyenne (moyenne supposée nulle) :

```
σ(t) = sqrt( 252 × Σ_{k=t-K+1..t} α(t-k+1) × r(k)²  /  Σ_{k=1..K} α(k) )

r(k) = ln( S(k) / S(k-1) )
α(k) = (1 - λ) × λ^(k-1)
```

- `S(k)` : valeur du sous-jacent au jour `k`
- `K` : nombre de jours de la fenêtre de calcul
- `λ` : facteur de décroissance
- `252` : annualisation

Deux volatilités sont calculées : `σS` (court terme, `λS`) et `σL` (long terme, `λL`), avec `λS < λL ≤ 1`. Si `λ = 1`, les poids sont égaux (moyenne simple).

### Volatilité retenue

```
σMAX(t) = max( σS(t), ..., σS(t-T+1), σL(t), ..., σL(t-T+1) )
```

### Exposition

La volatilité utilisée le jour `t` est celle calculée `d` jours plus tôt :

```
E(t) = min( LM, αT / σMAX(t-d) )
```

où `αT` est la volatilité cible.

### Valeur de l'indice

```
I(t) = I(t-1) × facteur(t)
```

| Indice | Facteur journalier |
|---|---|
| Price Return | `1 + E(t) × rU(t)` |
| Total Return | `1 + E(t) × rU(t) + (1 - E(t)) × rC(t)` |
| Excess Return | `1 + E(t) × (rU(t) - rC(t))` |

Rendement du cash, avec le taux de la veille et les jours calendaires écoulés :

```
rC(t) = r(t-1) × d(t, t-1) / DayCount
```

## Architecture

```
ConfigLoader ──► IndexParams ──► IndexFactory ──► indice
                     │
        ┌────────────┼──────────────┐
VolatilityEstimator  │      ReturnsCalculator
        └─► ExposureModel           │
                     ▼              ▼
              BaseVolTargetIndex  (E(t), rU(t))
              ├── PriceReturnIndex
              └── CashAwareIndex  (+ rC(t))
                  ├── TotalReturnIndex
                  └── ExcessReturnIndex
```

| Classe | Rôle |
|---|---|
| `IndexParams` | Paramètres de l'indice (dataclass immuable), validés à la construction |
| `ConfigLoader` | Lit le fichier JSON et fournit des `IndexParams` |
| `ReturnsCalculator` | Calcule les rendements du sous-jacent (logarithmique et simple) et du cash |
| `VolatilityEstimator` | Calcule `σS`, `σL` et `σMAX` |
| `ExposureModel` | Calcule l'exposition `E(t)` |
| `BaseVolTargetIndex` | Classe mère : attributs `exposure` et `underlying_returns`, méthode abstraite du facteur journalier, méthode `compute` qui renvoie la série de valeurs de l'indice |
| `PriceReturnIndex` | Facteur de l'indice Price Return |
| `CashAwareIndex` | Classe mère des indices utilisant le rendement du cash (attribut : série `rC`) |
| `TotalReturnIndex`, `ExcessReturnIndex` | Facteurs des indices Total et Excess Return |
| `IndexFactory` | Construit l'indice du bon type à partir du JSON |


## Paramètres

| Paramètre | Description |
|---|---|
| `index_type` | `price_return`, `total_return` ou `excess_return` |
| `vol_target` | Volatilité cible `αT` |
| `lam_S`, `lam_L` | Facteurs de décroissance court et long terme (`0 < lam_S < lam_L ≤ 1`) |
| `K` | Fenêtre de calcul des volatilités (jours) |
| `T` | Fenêtre du maximum des volatilités (jours) |
| `LM` | Exposition maximale (levier max) |
| `d` | Décalage (jours) |
| `cash_rate` | Taux de cash (ex. `SONIA`, `FedFunds`), requis pour `total_return` et `excess_return` |
| `day_count` | Convention de jours : `360` ou `365`, requis avec `cash_rate` |

Exemple de configuration (valeurs de l'Appendix C des Ground Rules, FTSE Divest-Invest Developed 200 USD) :

```json
{
  "FTSE Divest-Invest Developed 200 VT Excess Return USD": {
    "index_type": "excess_return",
    "vol_target": 0.12,
    "lam_S": 0.95,
    "lam_L": 0.98,
    "K": 120,
    "T": 5,
    "LM": 1,
    "d": 3,
    "cash_rate": "FedFunds",
    "day_count": 360
  }
}
```


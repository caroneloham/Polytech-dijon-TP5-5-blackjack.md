# Blackjack en Python

Jeu de blackjack dans le terminal, pour **1 à 7 joueurs**, contre la banque.

## Lancer le jeu

Python 3 doit être installé. Lance le fichier avec :

```bash
python blackjack.py
```

Adapte le nom si ton fichier s'appelle autrement.

## Règles

- Chaque joueur commence avec **100 jetons**.
- La mise est de **10 jetons par manche**.
- Le but est de se rapprocher de **21 sans le dépasser**.
- Un as vaut **1 ou 11**, les figures valent **10**.
- Un blackjack correspond à **21 points avec deux cartes**.
- La banque tire jusqu'à atteindre **17 points ou plus**.

## Actions disponibles

| Action | Effet |
|---|---|
| Se coucher | Abandonner et récupérer la moitié de la mise, seulement avant de tirer. |
| Doubler | Doubler la mise avant de tirer, si les jetons suffisent, recevoir une dernière carte et terminer son tour. |
| Tirer | Recevoir une carte supplémentaire. |
| Rester | Terminer son tour avec ses cartes actuelles. |

## Gains

Les montants suivants sont rendus **mise comprise** :

- **Victoire :** 2 fois la mise.
- **Blackjack :** 2,5 fois la mise.
- **Égalité :** mise remboursée.
- **Défaite :** mise perdue.

## Compatibilité

**`os.system("cls")` fonctionne sous Windows, mais n'est pas compatible avec Linux.** Pour effacer le terminal sous Windows, Linux et macOS, utilise :

```python
import os

os.system("cls" if os.name == "nt" else "clear")
```

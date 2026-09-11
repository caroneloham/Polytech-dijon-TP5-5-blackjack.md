# Black Jack

![Black Jack — Polytech Dijon](img/poly.png)

Jeu de blackjack en Python dans le terminal, pour **1 à 7 joueurs**, contre la banque.

## 📋 Consignes du TP

Retrouve le sujet et les exercices demandés ici :

**[Consulter les consignes du TP Blackjack](https://github.com/esirem-chassel/3aa-soutien/blob/main/TPs/5-blackjack.md)**

## Lancer le jeu

Installe **Python 3**, puis ouvre un terminal dans le dossier du projet et lance :

```bash
python main.py
```

Sous Linux ou macOS, utilise `python3 main.py` si nécessaire.

## Règles

- Chaque joueur commence avec **100 jetons** et mise **10 jetons par manche**.
- Le but est de se rapprocher de **21 sans le dépasser**.
- Les cartes de 2 à 9 valent leur nombre ; le 10 et les figures valent **10**.
- Un as vaut **1 ou 11**, selon ce qui avantage la main.
- Un blackjack correspond à **21 points avec les deux premières cartes**.
- La banque tire jusqu'à atteindre **17 points ou plus**.
- Les jetons sont conservés entre les manches. Avec moins de 10 jetons, un joueur ne peut plus participer.

## Actions disponibles

| Choix | Action | Effet |
| --- | --- | --- |
| 1 | Se coucher | Abandonner et récupérer la moitié de la mise, avant de tirer. |
| 2 | Doubler | Doubler la mise si les jetons suffisent, avant de tirer, puis recevoir une seule carte et terminer son tour. |
| 3 | Tirer | Recevoir une carte supplémentaire. |
| 4 | Rester | Terminer son tour avec ses cartes actuelles. |

## Gains

Les montants suivants sont rendus **mise comprise** :

- **Victoire :** 2 fois la mise.
- **Blackjack gagnant :** 2,5 fois la mise.
- **Égalité :** mise remboursée, y compris si le joueur et la banque ont un blackjack.
- **Défaite :** mise perdue.

## Compatibilité

**La commande `os.system("cls")` fonctionne sous Windows, mais n'est pas compatible avec Linux.** Pour adapter l'effacement du terminal à Windows, Linux et macOS, utilise :

```python
import os

os.system("cls" if os.name == "nt" else "clear")
```

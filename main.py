import random
import json
from math import ceil
from pathlib import Path

JETONS_DEPART = 100
MISE_MIN = 10
MISE_MAX = 50
MAX_JOUEURS = 7
FICHIER = Path(__file__).with_name(".sauvegarde.json")


def demander_nombre(message, minimum, maximum):
    while True:
        try:
            nombre = int(input(message))
            if minimum <= nombre <= maximum:
                return nombre
        except ValueError:
            pass
        print("Met un nombre entre", minimum, "et", maximum)


def sauvegarder(joueurs):
    donnees = {}
    for nom, joueur in joueurs.items():
        donnees[nom] = {
            "nom": nom,
            "jetons": joueur["jetons"],
            "mise_max": joueur["mise_max"]
        }
    with open(FICHIER, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, ensure_ascii=False, indent=2)


def charger():
    if not FICHIER.exists():
        return {}
    with open(FICHIER, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def create_player(nom):
    return {
        "nom": nom,
        "jetons": JETONS_DEPART,
        "mise_max": MISE_MAX
    }


def newgame(joueurs):
    nb = demander_nombre("Vous ete combien de joueur (1 à 7) : ", 1, MAX_JOUEURS)
    actifs = []
    noms = []
    for i in range(nb):
        while True:
            nom = input("C quoi ton nom : ").strip()
            if nom and nom not in noms:
                break
            print("Met un nom different pour chaque joueur.")
        noms.append(nom)
        if nom not in joueurs:
            joueurs[nom] = create_player(nom)
        joueur = joueurs[nom]
        if joueur["jetons"] < MISE_MIN:
            print(nom, "a plus asser de jetons pour joué.")
            continue
        maximum = int(min(joueur["mise_max"], joueur["jetons"]))
        print(nom, "a", joueur["jetons"], "jetons.")
        joueur["mise"] = demander_nombre("Ta mise : ", MISE_MIN, maximum)
        joueur["jetons"] -= joueur["mise"]
        actifs.append(joueur)
    return actifs


def score(main):
    total = sum(main)
    nb_as = main.count(11)

    while total > 21 and nb_as > 0:
        total -= 10
        nb_as -= 1
    return total


def blackjack(main):
    return len(main) == 2 and score(main) == 21


def assurance(joueurs, banque):
    if banque[0] != 11:
        return
    for joueur in joueurs:
        joueur["assurance"] = 0
        prix = ceil(joueur["mise"] / 2)
        if joueur["jetons"] < prix:
            print(joueur["nom"], "a pas asser pour l'assurance.")
            continue
        print(joueur["nom"], ": assurance pour", prix, "jetons.")
        while True:
            choix = input("Tu prend l'assurance ? (o/n) : ").strip().lower()
            if choix in ["o", "n"]:
                break
            print("Repond o ou n.")
        if choix == "o":
            joueur["jetons"] -= prix
            joueur["assurance"] = prix
    for joueur in joueurs:
        if joueur["assurance"]:
            if blackjack(banque):
                gain = joueur["assurance"] * 2
                joueur["jetons"] += gain
                print(joueur["nom"], "assurance gagnée :", gain, "jetons rendus.")
            else:
                print(joueur["nom"], "assurance perdue.")


def player_turn(joueur, paquet):
    numero = 0
    while numero < len(joueur["mains"]):
        main_joueur = joueur["mains"][numero]
        while score(main_joueur["main"]) < 21:
            cartes = main_joueur["main"]
            print("\n", joueur["nom"], "main", numero + 1, ":", cartes)
            print("Ta ce score :", score(cartes))
            choix = input("1) Se coucher  2) Doubler  3) Tirer  4) Rester  5) Split : ")
            if choix == "1":
                if len(cartes) == 2:
                    joueur["jetons"] += main_joueur["mise"] / 2
                    main_joueur["couche"] = True
                    break
                print("Ta deja tirer tu peut plus te coucher.")
            elif choix == "2":
                if len(cartes) != 2:
                    print("Tu peut plus doubler ta mise.")
                elif joueur["jetons"] < main_joueur["mise"]:
                    print("Ta pas asser de jetons.")
                else:
                    joueur["jetons"] -= main_joueur["mise"]
                    main_joueur["mise"] *= 2
                    cartes.append(paquet.pop())
                    break
            elif choix == "3":
                cartes.append(paquet.pop())
            elif choix == "4":
                break
            elif choix == "5":
                if len(cartes) != 2 or cartes[0] != cartes[1]:
                    print("Il faut deux cartes de meme valeur.")
                elif len(joueur["mains"]) != 1:
                    print("Un seul split par manche.")
                elif joueur["jetons"] < main_joueur["mise"]:
                    print("Ta pas asser de jetons pour split.")
                else:
                    joueur["jetons"] -= main_joueur["mise"]
                    carte = cartes.pop()
                    cartes.append(paquet.pop())
                    main_joueur["split"] = True
                    joueur["mains"].append({
                        "main": [carte, paquet.pop()],
                        "mise": main_joueur["mise"],
                        "couche": False,
                        "split": True
                    })
            else:
                print("Met un choix entre 1 et 5.")
        print(joueur["nom"], "main", numero + 1, main_joueur["main"],
              "Score :", score(main_joueur["main"]))
        numero += 1


def win_condition(joueurs, banque):
    for joueur in joueurs:
        for numero, main_joueur in enumerate(joueur["mains"], 1):
            points = score(main_joueur["main"])
            mise = main_joueur["mise"]
            naturel = blackjack(main_joueur["main"]) and not main_joueur["split"]
            gain = 0
            if main_joueur["couche"]:
                resultat = "tu t'es coucher"
            elif points > 21:
                resultat = "ta depasser 21"
            elif blackjack(banque):
                if naturel:
                    gain = mise
                    resultat = "egaliter"
                else:
                    resultat = "la banque a un blackjack ta perdu"
            elif naturel:
                gain = mise * 2.5
                resultat = "blackjack ta bien jouer !"
            elif score(banque) > 21 or points > score(banque):
                gain = mise * 2
                resultat = "ta gagner !"
            elif points == score(banque):
                gain = mise
                resultat = "egaliter"
            else:
                resultat = "ta perdu"
            joueur["jetons"] += gain
            if gain > mise:
                joueur["mise_max"] *= 2
            print(joueur["nom"], "main", numero, ":", resultat)
        print("Il te reste sa en jetons :", joueur["jetons"])


def jouer_manche(joueurs):
    actifs = newgame(joueurs)
    if not actifs:
        print("Ya personne qui peut joué.")
        return
    paquet = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 24
    random.shuffle(paquet)
    for joueur in actifs:
        joueur["mains"] = [{
            "main": [paquet.pop(), paquet.pop()],
            "mise": joueur["mise"],
            "couche": False,
            "split": False
        }]
    banque = [paquet.pop(), paquet.pop()]
    print("La carte qu'on voit de la banque :", banque[0])
    for joueur in actifs:
        print(joueur["nom"], ":", joueur["mains"][0]["main"])
    assurance(actifs, banque)
    if not blackjack(banque):
        for joueur in actifs:
            player_turn(joueur, paquet)
    while score(banque) <= 16:
        banque.append(paquet.pop())
    print("Banque :", banque, "Score :", score(banque))
    win_condition(actifs, banque)
    sauvegarder(joueurs)


def menu():
    try:
        joueurs = charger()
    except (OSError, ValueError):
        print("Sauvegarde illisible, garde le fichier pour le verifier.")
        return
    while True:
        print("1 - Jouer une manche")
        print("2 - Quitter")
        choix = input("Ton choix : ").strip()
        if choix == "1":
            jouer_manche(joueurs)
        elif choix == "2":
            return
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu()

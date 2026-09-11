import random
import os
#ce programme ne marche que sous windows, la raison c import os je l'utilise pour nettoyer le terminal (marche pas dans l'IDE dois être start en cmd) avec la commande cls de windows j'aurias pu faire quen fonciton de l'os il passe de CLS a Clear avec une varible qui try exept... mais bon..
print("Ce programme ne marche que sous windows ")
def create_player():
    return {
        "nom": input("C quoi ton nom : "),
        "jetons": 100,
        "main": [],
        "mise": 10,
        "couche": False
    }


def newgame():
    while True:
        try:
            os.system("cls")
            nb = int(input("Vous ete combien de joueur (1 à 7) : "))
            if 1 <= nb <= 7:
                break
        except ValueError:
            pass
        print("Met un nombre entre 1 et 7 stp.")
        os.system("cls")

    joueurs = []
    for i in range(nb):
        joueurs.append(create_player())
    return joueurs


def score(main):
    total = sum(main)
    nb_as = main.count(11)

    while total > 21 and nb_as > 0:
        total -= 10
        nb_as -= 1
    return total


def blackjack(main):
    return len(main) == 2 and score(main) == 21


def player_turn(joueur, paquet):
    while score(joueur["main"]) < 21:
        print("\n", joueur["nom"], joueur["main"])
        print("Ta ce score :", score(joueur["main"]))
        choix = input("1) Se coucher  2) Doubler  3) Tirer  4) Rester : ")
        os.system("cls")
        if choix == "1":
            if len(joueur["main"]) == 2:
                joueur["jetons"] += joueur["mise"] / 2
                joueur["couche"] = True
                break
            print("Ta deja tirer tu peut plus te coucher.")

        elif choix == "2":
            if len(joueur["main"]) != 2:
                print("Tu peut plus doubler ta mise.")
            elif joueur["jetons"] < joueur["mise"]:
                print("Ta pas asser de jetons.")
            else:
                joueur["jetons"] -= joueur["mise"]
                joueur["mise"] *= 2
                joueur["main"].append(paquet.pop())
                break

        elif choix == "3":
            joueur["main"].append(paquet.pop())

        elif choix == "4":
            break

        else:
            print("On a dit entre 1 et 4 pelo.")

    print(joueur["nom"], joueur["main"], "Score :", score(joueur["main"]))


def win_condition(joueurs, banque):
    # joueur prend chaque joueur de la liste, un par un
    for joueur in joueurs:
        points = score(joueur["main"])
        mise = joueur["mise"]
        gain = 0

        if joueur["couche"]:
            resultat = "tu t'es coucher"

        elif points > 21:
            resultat = "ta depasser 21"

        elif blackjack(banque):
            if blackjack(joueur["main"]):
                gain = mise
                resultat = "egaliter"
            else:
                resultat = "la banque a un blackjack ta perdu"

        elif blackjack(joueur["main"]):
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
        print(joueur["nom"], ":", resultat)
        print("Il te reste sa en jetons :", joueur["jetons"])


joueurs = newgame()

while True:
    # 11 = As meno
    paquet = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 24
    random.shuffle(paquet)
    actifs = []

    for joueur in joueurs:
        if joueur["jetons"] >= 10:
            joueur["mise"] = 10
            joueur["jetons"] -= 10
            joueur["couche"] = False
            joueur["main"] = [paquet.pop(), paquet.pop()]
            actifs.append(joueur)
        else:
            print(joueur["nom"], "a plus asser de jetons pour joué.")

    if not actifs:
        print("Ya plus personne qui peut joué.")
        break

    banque = [paquet.pop(), paquet.pop()]
    print("\nOn mise 10 jetons")
    print("La carte qu'on voit de la banque : ", banque[0])

    for joueur in actifs:
        print(joueur["nom"], ":", joueur["main"])

    if not blackjack(banque):
        for joueur in actifs:
            player_turn(joueur, paquet)

    while score(banque) <= 16:
        banque.append(paquet.pop())

    print("\nBanque :", banque, "Score :", score(banque))
    win_condition(actifs, banque)

    if input("\nOn refait une parti ? (o/n) : ").lower() != "o":
        break
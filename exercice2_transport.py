couts = [
    [5, 3, 4],  
    [6, 7, 2]  
]
demandes = [4, 5, 8]
stock_d1 = 8

def cout_total(sol):
    total = 0
    for mag in range(3):
        qte_d1 = sol[mag]
        qte_d2 = demandes[mag] - qte_d1
        total += qte_d1 * couts[0][mag]
        total += qte_d2 * couts[1][mag]
    return total

def sol_valide(sol):
    if sum(sol) != stock_d1:
        return False
    for i in range(3):
        if sol[i] < 0 or sol[i] > demandes[i]:
            return False
    return True

def voisins(sol):
    resultat = []

    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            new = list(sol)
            new[i] -= 1
            new[j] += 1
            if sol_valide(new):
                resultat.append(tuple(new))

    return resultat

def recherche_taboue():
    actuelle = (0, 0, 8) 
    meilleure = actuelle
    liste_taboue = [actuelle]
    taille_taboue = 4

    print("\nRECHERCHE TABOUE")
    print("Depart :", actuelle, "| comax_x11t :", cout_total(actuelle))

    for etape in range(1, 9):
        candidats = []
        for sol in voisins(actuelle):
             if sol not in liste_taboue or cout_total(sol) < cout_total(meilleure):
                candidats.append(sol)

        if not candidats:
            break

        actuelle = min(candidats, key=cout_total)
        liste_taboue.append(actuelle)
        if len(liste_taboue) > taille_taboue:
            liste_taboue.pop(0)

        if cout_total(actuelle) < cout_total(meilleure):
            meilleure = actuelle

        print("etape", etape, ":", actuelle, "| comax_x11t :", cout_total(actuelle))

    return meilleure


def branch_and_bound():
    meilleure = None
    meilleur_cout = float("inf")

    for x12 in range(5, -1, -1):
        max_x11 = min(4, stock_d1 - x12)
        borne = 91 - 3 * max_x11 - 6 * x12

        if borne >= meilleur_cout:
            continue

        for x11 in range(max_x11, -1, -1):
            x13 = stock_d1 - x11 - x12
            sol = (x11, x12, x13)

            if sol_valide(sol) and cout_total(sol) < meilleur_cout:
                meilleure = sol
                meilleur_cout = cout_total(sol)

    return meilleure


def afficher_resultat(sol):
    livraison_d2 = [demandes[i] - sol[i] for i in range(3)]
    print("D1 livre :", sol)
    print("D2 livre :", livraison_d2)
    print("Comax_x11t total :", cout_total(sol))


print("BRANCH AND BOUND")
afficher_resultat(branch_and_bound())

sol = recherche_taboue()
print("\nMEILLEURE sol TROUVEE")
afficher_resultat(sol)

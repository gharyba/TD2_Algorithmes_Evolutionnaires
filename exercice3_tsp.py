import math
import random

distances = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17,
    (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9, (7, 8): 13
}

depart = (2, 3, 4, 5, 6, 7, 8)


def cout_circuit(circuit):
    trajet = [1] + list(circuit) + [1]
    total = 0
    for i in range(len(trajet) - 1):
        a, b = trajet[i], trajet[i + 1]
        distance = distances.get(tuple(sorted((a, b))))
        if distance is None:
            return math.inf
        total += distance
    return total


def afficher(circuit):
    trajet = [1] + list(circuit) + [1]
    print(" -> ".join(map(str, trajet)), "| coût :", cout_circuit(circuit))


def voisins(circuit):
    resultat = []
    n = len(circuit)

    for i in range(n - 1):
        for j in range(i + 1, n):
            nouveau = circuit[:i] + circuit[i:j + 1][::-1] + circuit[j + 1:]
            if cout_circuit(nouveau) != math.inf and nouveau not in resultat:
                resultat.append(nouveau)
    return resultat


def recherche_taboue():
    actuelle = depart
    meilleure = depart
    tabous = [depart]

    for etape in range(1, 21):
        candidats = []
        for solution in voisins(actuelle):
            if solution not in tabous or cout_circuit(solution) < cout_circuit(meilleure):
                candidats.append(solution)

        if not candidats:
            break

        actuelle = min(candidats, key=cout_circuit)
        tabous.append(actuelle)
        if len(tabous) > 5:
            tabous.pop(0)

        if cout_circuit(actuelle) < cout_circuit(meilleure):
            meilleure = actuelle

        print("Étape", etape, "| coût actuel :", cout_circuit(actuelle),
              "| meilleur :", cout_circuit(meilleure))
    return meilleure


def recuit_simule():
    random.seed(23)  
    actuelle = depart
    meilleure = depart
    temperatures = [10, 8, 6, 4, 2]  

    for etape, temperature in enumerate(temperatures, start=1):
        candidat = random.choice(voisins(actuelle))
        difference = cout_circuit(candidat) - cout_circuit(actuelle)

        if difference <= 0:
            probabilite = 1
        else:
            probabilite = math.exp(-difference / temperature)

        if random.random() < probabilite:
            actuelle = candidat
            decision = "accepté"
        else:
            decision = "refusé"

        if cout_circuit(actuelle) < cout_circuit(meilleure):
            meilleure = actuelle

        print("Étape", etape, "| T =", temperature,
              "|", decision, "| meilleur :", cout_circuit(meilleure))

    return meilleure


def circuit_aleatoire():
    while True:
        circuit = tuple(random.sample(range(2, 9), 7))
        if cout_circuit(circuit) != math.inf:
            return circuit


def croisement(parent1, parent2):
    coupe = random.randint(1, 6)
    enfant = list(parent1[:coupe])
    for ville in parent2:
        if ville not in enfant:
            enfant.append(ville)
    return tuple(enfant)


def mutation(circuit):
    nouveau = list(circuit)
    i, j = random.sample(range(7), 2)
    nouveau[i], nouveau[j] = nouveau[j], nouveau[i]
    return tuple(nouveau)


def algorithme_genetique():
    random.seed(42)
    population = [depart]
    while len(population) < 30:
        population.append(circuit_aleatoire())

    meilleure = min(population, key=cout_circuit)

    for generation in range(1, 61):
        population.sort(key=cout_circuit)
        nouvelle_population = population[:2]  

        while len(nouvelle_population) < 30:
            parent1 = random.choice(population[:10])
            parent2 = random.choice(population[:10])
            enfant = croisement(parent1, parent2)

            if random.random() < 0.20:
                enfant = mutation(enfant)

            if cout_circuit(enfant) == math.inf:
                enfant = parent1

            nouvelle_population.append(enfant)

        population = nouvelle_population
        candidat = min(population, key=cout_circuit)
        if cout_circuit(candidat) < cout_circuit(meilleure):
            meilleure = candidat

        if generation % 10 == 0:
            print("Génération", generation, "| meilleur :", cout_circuit(meilleure))

    return meilleure


print("CIRCUIT INITIAL")
afficher(depart)

print("\nRECHERCHE TABOUE")
afficher(recherche_taboue())

print("\nRECUIT SIMULE (5 ITERATIONS)")
afficher(recuit_simule())

print("\nALGORITHME GENETIQUE")
afficher(algorithme_genetique())

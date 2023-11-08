from fuzzywuzzy import fuzz
from utils.Constants import LOCATIVAS, LABORATORIOS, SANITARIAS, SANEAMIENTO, GESTION_RIESGO

# Establece un umbral de similitud para agrupar valores
SIMILAR_AVERAGE = 60


def groupSimilarConcepts(concepts):
    grouped_concepts = {}

    for concept in concepts:
        found = False
        for grouped_concept in grouped_concepts:
            if fuzz.ratio(concept, grouped_concept) >= SIMILAR_AVERAGE:
                grouped_concepts[grouped_concept].append(concept)
                found = True
                break
        if not found:
            grouped_concepts[concept] = [concept]

    return grouped_concepts


def totalValue(title_component, code):
    if title_component == LOCATIVAS:
        return 30
    if title_component == LABORATORIOS:
        return 10
    if title_component == SANITARIAS:
        return 25
    if title_component == SANEAMIENTO and code == "EE":
        return 25
    elif title_component == SANEAMIENTO and code == "ESL":
        return 30
    if title_component == GESTION_RIESGO and code == "EE":
        return 10
    elif title_component == GESTION_RIESGO and code == "ESL":
        return 15

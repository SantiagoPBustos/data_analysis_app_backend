from fuzzywuzzy import fuzz
from utils.Constants import GENERAL, LOCATIVAS, LABORATORIOS, SANITARIAS, SANEAMIENTO, GESTION_RIESGO, GENERAL_MODAL, LOCATIVAS_MODAL, LABORATORIOS_MODAL, SANITARIAS_MODAL, SANEAMIENTO_MODAL, GESTION_RIESGO_MODAL

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

def titleComponent(title_component, code):
    if title_component == GENERAL_MODAL:
        return [GENERAL, 100, GENERAL]
    if title_component == LOCATIVAS_MODAL:
        return [LOCATIVAS, 30, "2."]
    if title_component == LABORATORIOS_MODAL:
        return [LABORATORIOS, 10, "3."]
    if title_component == SANITARIAS_MODAL:
        return [SANITARIAS, 25, "4.0"]    
    if title_component == SANEAMIENTO_MODAL and code == "EE":
        return [SANEAMIENTO, 25, "4.1"]    
    elif title_component == SANEAMIENTO_MODAL and code == "ESL":
        return [SANEAMIENTO, 30, "4.1"] 
    if title_component == GESTION_RIESGO_MODAL and code == "EE":
        return [GESTION_RIESGO, 10, "5."] 
    elif title_component == GESTION_RIESGO_MODAL and code == "ESL":
        return [GESTION_RIESGO, 15, "5."]

def areAllZero(array):
    return None if all(value == 0 for _, value in array) else False

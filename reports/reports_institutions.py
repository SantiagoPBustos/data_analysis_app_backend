from collections import defaultdict
from utils.utilities import groupSimilarConcepts, totalValue

# Informe general del número total de instituciones cargadas


def countTotalInstitutions(data):
    try:
        elements = data.get("data", [])
        uniqueID = set()

        for element in elements:
            id = element.get("ID")
            if id is not None:
                uniqueID.add(id)

        return len(uniqueID)

    except Exception as e:
        return str(e)

# Informe general del número total de instituciones cargadas filtrado por tipo


def countInstitutionsByTypePlace(data, type):
    try:
        elements = data.get("data", [])
        count = 0

        for element in elements:
            tipo = element.get("TIPO DE ESTABLECIMIENTO", "").strip().upper()
            if tipo == type.upper():
                count += 1

        return count

    except Exception as e:
        return str(e)


# Calcula promedio de los peores porcentajes de cumplimiento agrupados por municipio
def worstAveragesByMunicipality(data):
    try:
        elements = data.get("data", [])
        averages_by_municipality = defaultdict(list)

        # Recorre los elementos y agrupa por municipio y acumula los valores de cumplimiento
        for element in elements:
            municipality = element.get("MUNICIPIO")
            compliance = element.get("% DE CUMPLIMIENTO")

            try:
                compliance = float(compliance)
                if compliance.is_integer() and compliance > 100:
                    compliance /= 10.0
            except ValueError:
                continue

            if municipality:
                averages_by_municipality[municipality].append(compliance)

        # Calcula el promedio para cada municipio
        result = []
        for municipality, compliances in averages_by_municipality.items():
            average = round(sum(compliances) / len(compliances))
            result.append([municipality, average])

        sorted_result = sorted(result, key=lambda x: x[1])
        limited_result = sorted_result[:12]
        return limited_result

    except Exception as e:
        return str(e)

# Calcula promedio de los peores porcentajes de cumplimiento agrupados por tipo de institucion


def worstAveragesByTypeInstitution(data):
    try:
        elements = data.get("data", [])
        averages_by_type = defaultdict(list)

        # Recorre los elementos y agrupa por tipo de establecimiento y acumula los valores de cumplimiento
        for element in elements:
            tipo_establecimiento = element.get("TIPO DE ESTABLECIMIENTO")
            cumplimiento = element.get("% DE CUMPLIMIENTO")

            try:
                cumplimiento = float(cumplimiento)
                if cumplimiento.is_integer() and cumplimiento > 100:
                    cumplimiento /= 10.0
            except ValueError:
                continue

            if tipo_establecimiento:
                averages_by_type[tipo_establecimiento].append(cumplimiento)

        # Calcula el promedio para cada tipo de establecimiento y redondea a un decimal
        result = []
        for tipo, cumplimientos in averages_by_type.items():
            average = round(sum(cumplimientos) / len(cumplimientos), 1)
            result.append([tipo, average])

        result_sorted = sorted(result, key=lambda x: x[1])
        return result_sorted

    except Exception as e:
        return str(e)

# Calcula promedio de los peores porcentajes de cumplimiento agrupados por componente segun municipio


def worstAveragesPerComponentByMunicipality(data, start, title_component, limit):
    try:
        records = data.get("data", [])
        dictionary = defaultdict(list)

        # Recorre los elementos y agrupa por municipio y acumula los valores de cumplimiento
        for record in records:
            try:
                sum_values = 0
                for key, value in record.items():
                    if key.startswith(start) and (key != title_component):
                        sum_values += float(value)

                code = record.get("CÓDIGO SECRETARIA DE SALUD")
                total_value = totalValue(title_component, code)

                record[title_component] = round((sum_values/total_value)*100)
                municipality = record.get("MUNICIPIO")
                compliance = record.get(title_component)
                dictionary[municipality].append(compliance)
            except ValueError:
                continue

        # Calcula el promedio para cada municipio
        result = []
        for municipality, compliances in dictionary.items():
            average = round(sum(compliances) / len(compliances))
            result.append([municipality, average])

        sorted_result = sorted(result, key=lambda x: x[1])
        result = sorted_result[:limit]
        return result

    except Exception as error:
        return str(error)

# Calcular promedio agrupado por porcentaje de cumplimiento de instituciones


def calculateAverageBySanitaryConcept(data):
    # Extraer la lista de registros de la clave "data"
    registros = data["data"]
    concepts = [registro["CONCEPTO"] for registro in registros]

    # Agrupa valores similares en conceptos
    grouped_concepts = groupSimilarConcepts(concepts)

    total_registros = len(registros)

    porcentajes = [
        {
            "name": conceptos[0],
            "y": (len(conceptos) / total_registros) * 100,
        }
        for conceptos in grouped_concepts.values()
    ]

    return porcentajes

from collections import defaultdict
from utils.utilities import groupSimilarConcepts, totalValue, titleComponent, areAllZero

# Elimina las instituciones que tienen mas de 1 visita para solo tener en cuenta la ultimo registro


def deleteDuplicateRecords(data):
    records = data["data"]
    dictionary_records = {}
    duplicate_records = []

    for registro in records:
        try:
            inscripcion = str(registro.get(
                "INSCRIPCIÓN CÓDIGO DANE O NIT", ""))

            if inscripcion in dictionary_records:
                dictionary_records[inscripcion] = registro
                duplicate_records.append(registro)
            else:
                dictionary_records[inscripcion] = registro
        except ValueError:
            continue

    records_without_duplicates = list(dictionary_records.values())
    result = {"data": records_without_duplicates}
    return result

# Informe de cantidad de instituciones rurales cargadas


def countTotalRural(data):
    data = deleteDuplicateRecords(data)
    records = data["data"]
    countRural = 0

    for registro in records:
        if registro.get("UBICACIÓN", "").upper() == "VEREDA":
            countRural += 1

    return countRural

# Informe general del número total de instituciones cargadas


def countTotalInstitutions(data):
    data = deleteDuplicateRecords(data)
    try:
        elements = data.get("data", [])
        totalElements = len(elements)
        return totalElements

    except Exception as e:
        return str(e)

# Informe general del número total de instituciones cargadas filtrado por tipo


def countInstitutionsByTypePlace(data, type):
    data = deleteDuplicateRecords(data)
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
    data = deleteDuplicateRecords(data)
    try:
        elements = data.get("data", [])
        averages_by_municipality = defaultdict(list)
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
        result = []
        for municipality, compliances in averages_by_municipality.items():
            average = round(sum(compliances) / len(compliances))
            result.append([municipality, average])

        sorted_result = sorted(result, key=lambda x: x[1])
        return sorted_result

    except Exception as e:
        return str(e)

# Calcula promedio de los peores porcentajes de cumplimiento agrupados por tipo de institucion


def worstAveragesByTypeInstitution(data):
    data = deleteDuplicateRecords(data)
    try:
        elements = data.get("data", [])
        averages_by_type = defaultdict(list)
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
        result = []
        for tipo, cumplimientos in averages_by_type.items():
            average = round(sum(cumplimientos) / len(cumplimientos), 1)
            result.append([tipo, average])

        result_sorted = sorted(result, key=lambda x: x[1])
        return result_sorted

    except Exception as e:
        return str(e)

# Calcula promedio de los peores porcentajes de cumplimiento agrupados por componente segun municipio


def worstAveragesPerComponentByMunicipality(data, start, title_component):
    data = deleteDuplicateRecords(data)
    try:
        records = data.get("data", [])
        dictionary = defaultdict(list)
        for record in records:
            try:
                sum_values = 0
                for key, value in record.items():
                    if key.startswith(start) and (key != title_component):
                        sum_values += float(value)

                code = record.get("CÓDIGO SECRETARIA DE SALUD")
                total_value = totalValue(title_component, code)

                record[title_component] = round((sum_values*100)/total_value)
                municipality = record.get("MUNICIPIO")
                compliance = record.get(title_component)
                dictionary[municipality].append(compliance)
            except ValueError:
                continue
        result = []
        for municipality, compliances in dictionary.items():
            average = round(sum(compliances) / len(compliances))
            result.append([municipality, average])

        sorted_result = sorted(result, key=lambda x: x[1])
        aux = areAllZero(sorted_result)
        if aux == False:
            return sorted_result
        elif aux == None:
            return None

    except Exception as error:
        return str(error)

# Calcular promedio agrupado por porcentaje de cumplimiento de instituciones


def calculateAverageBySanitaryConcept(data):
    try:
        data = deleteDuplicateRecords(data)
        registros = data["data"]
        concepts = [registro["CONCEPTO"] for registro in registros]
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
    except Exception as error:
        return str(error)

# Informe de las instituciones con porcentaje de cumplimiento segun municipio y componente


def institutionsForMunicipalityPerComponent(data, municipality, component):
    data = deleteDuplicateRecords(data)
    result = []
    try:
        records = [
            record for record in data["data"] if record["MUNICIPIO"] == municipality]
        try:
            for record in records:
                code = record.get("CÓDIGO SECRETARIA DE SALUD")
                title = titleComponent(component, code)

                sum_values = 0
                for key, value in record.items():
                    if key.startswith(title[2]) and title[2] == "% DE CUMPLIMIENTO":
                        sum_values = float(value)
                    elif key.startswith(title[2]) and (key != title[0]):
                        sum_values += float(value)

                cumplimiento = round((sum_values/title[1])*100)

                result.append([
                    f"{record['RAZÓN SOCIAL']} - {record['SEDE']}", cumplimiento])

        except ValueError:
            print(ValueError)

        data = sorted(result, key=lambda x: x[1])
        return data

    except Exception as error:
        return str(error)


def obtener_registros_por_municipio(data, municipio):
    data = deleteDuplicateRecords(data)
    try:
        registros_municipio = [
            registro for registro in data["data"] if registro["MUNICIPIO"] == municipio]
        return registros_municipio
    except Exception as error:
        return str(error)

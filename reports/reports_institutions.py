from collections import defaultdict
from utils.utilities import groupSimilarConcepts, totalValue

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
        limited_result = sorted_result[:20]
        return limited_result

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


def worstAveragesPerComponentByMunicipality(data, start, title_component, limit):
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

                record[title_component] = round((sum_values/total_value)*100)
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
        result = sorted_result[:limit]
        aux = areAllZero(result)
        if aux == False:
            return result
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

def obtener_registros_por_municipio(data, municipio):
    data = deleteDuplicateRecords(data)
    try:
        # Filtrar los registros por el municipio especificado
        registros_municipio = [
            registro for registro in data["data"] if registro["MUNICIPIO"] == municipio]

        # Convertir "% DE CUMPLIMIENTO" a números antes de ordenar
        registros_municipio = [
            {"% DE CUMPLIMIENTO": int(
                registro["% DE CUMPLIMIENTO"]), **registro}
            for registro in registros_municipio
        ]

        # Ordenar los registros por % DE CUMPLIMIENTO de menor a mayor
        registros_ordenados = sorted(
            registros_municipio, key=lambda x: x["% DE CUMPLIMIENTO"])

        # Eliminar la columna temporal "% DE CUMPLIMIENTO" creada para la comparación
        for registro in registros_ordenados:
            del registro["% DE CUMPLIMIENTO"]

        result = registros_ordenados[:10]
        return result

    except Exception as error:
        return str(error)


def obtener_razon_cumplimiento_formato_lista(data, municipio):
    data = deleteDuplicateRecords(data)
    try:
        # Filtrar los registros por el municipio especificado
        registros_municipio = [
            registro for registro in data["data"] if registro["MUNICIPIO"] == municipio]
        try:

            # Obtener la "RAZÓN SOCIAL" y el "% DE CUMPLIMIENTO" como una lista de listas
            datos_razon_cumplimiento = [
                [f"{registro['RAZÓN SOCIAL']} - {registro['SEDE']}", float(registro["% DE CUMPLIMIENTO"])] for registro in registros_municipio]
        except ValueError:
            print(ValueError)
        # Ordenar la lista por % DE CUMPLIMIENTO de menor a mayor
        datos_ordenados = sorted(datos_razon_cumplimiento, key=lambda x: x[1])
        result = datos_ordenados[:50]
        return result

    except Exception as error:
        return str(error)


def areAllZero(array):
    return None if all(value == 0 for _, value in array) else False

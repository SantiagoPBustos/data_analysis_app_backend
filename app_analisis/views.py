# Create your views here.
from django.http import JsonResponse
from reports.reports_institutions import countTotalRural, countTotalInstitutions, countInstitutionsByTypePlace, worstAveragesByMunicipality, worstAveragesByTypeInstitution, worstAveragesPerComponentByMunicipality, calculateAverageBySanitaryConcept, institutionsForMunicipalityPerComponent, obtener_registros_por_municipio
from utils.Constants import IE, IEES, HI, CDI, CER, LOCATIVAS, LABORATORIOS, SANITARIAS, SANEAMIENTO, GESTION_RIESGO

from rest_framework.views import APIView


class Data(APIView):
    def post(self, request):
        # Accede al JSON recibido en la solicitud POST
        data = request.data

        # Crea una respuesta JSON
        response = JsonResponse(
            {
                "status": 200,
                "total": countTotalInstitutions(data),
                "total_IE": countInstitutionsByTypePlace(data, IE),
                "total_IEES": countInstitutionsByTypePlace(data, IEES),
                "total_HI": countInstitutionsByTypePlace(data, HI),
                "total_CDI": countInstitutionsByTypePlace(data, CDI),
                "total_CER": countTotalRural(data),
                "worst_municipalities": worstAveragesByMunicipality(data),
                "type_institutions": worstAveragesByTypeInstitution(data),
                "location_conditions": worstAveragesPerComponentByMunicipality(data, "2.", LOCATIVAS, 20),
                "conditions_laboratories": worstAveragesPerComponentByMunicipality(data, "3.", LABORATORIOS, 20),
                "sanitary_conditions": worstAveragesPerComponentByMunicipality(data, "4.0", SANITARIAS, 20),
                "conditions_sanitation": worstAveragesPerComponentByMunicipality(data, "4.1", SANEAMIENTO, 20),
                "risk_management": worstAveragesPerComponentByMunicipality(data, "5.", GESTION_RIESGO, 35),
                "type_concept": calculateAverageBySanitaryConcept(data)
            }
        )

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"

        return response


class DataInstitution(APIView):
    def post(self, request):
        # Accede al JSON recibido en la solicitud POST
        datas = request.data.get('data', None)
        municipality = request.data.get('municipio', None)
        component = request.data.get('component', None)

        # Crea una respuesta JSON
        response = JsonResponse(
            {
                "status": 200,
                "reports": institutionsForMunicipalityPerComponent(datas, municipality, component),
                "data": obtener_registros_por_municipio(datas, municipality),
            }
        )

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"

        return response

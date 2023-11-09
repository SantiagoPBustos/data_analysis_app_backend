# Create your views here.
from django.http import JsonResponse
from reports.reports_institutions import countTotalInstitutions, countInstitutionsByTypePlace, worstAveragesByMunicipality, worstAveragesByTypeInstitution, worstAveragesPerComponentByMunicipality, calculateAverageBySanitaryConcept
from utils.Constants import IE, IEES, HI, CDI, CER, LOCATIVAS, LABORATORIOS, SANITARIAS, SANEAMIENTO, GESTION_RIESGO

from rest_framework.views import APIView
from rest_framework.response import Response


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
                "total_CER": countInstitutionsByTypePlace(data, CER),
                "worst_municipalities": worstAveragesByMunicipality(data),
                "type_institutions": worstAveragesByTypeInstitution(data),
                "location_conditions": worstAveragesPerComponentByMunicipality(data, "2.", LOCATIVAS, 20),
                "conditions_laboratories": worstAveragesPerComponentByMunicipality(data, "3.", LABORATORIOS, 20),
                "sanitary_conditions": worstAveragesPerComponentByMunicipality(data, "4.0", SANITARIAS, 12),
                "conditions_sanitation": worstAveragesPerComponentByMunicipality(data, "4.1", SANEAMIENTO, 12),
                "risk_management": worstAveragesPerComponentByMunicipality(data, "5.", GESTION_RIESGO, 20),
                "type_concept": calculateAverageBySanitaryConcept(data),
            }
        )

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"

        return response

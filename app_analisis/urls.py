from django.urls import path
from .views import Data, DataInstitution

urlpatterns = [
    path('postData/', Data.as_view(), name='postData'),    
    path('dataInstitution/', DataInstitution.as_view(), name='dataInstitution'),
]

from django.urls import path
from .views import Data

urlpatterns = [
    path('postData/', Data.as_view(), name='postData'),
]

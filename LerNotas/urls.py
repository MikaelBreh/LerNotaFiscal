from django.urls import path
from .views import SubirNota

urlpatterns = [
    path('', SubirNota, name='subir_nota'),

]

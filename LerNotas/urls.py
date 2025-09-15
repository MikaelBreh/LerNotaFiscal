from django.urls import path
from .views import SubirNota, upload_nota_fiscal

urlpatterns = [
    path('', SubirNota, name='subir_nota'),
    path('upload/', upload_nota_fiscal, name='upload_nota_fiscal'),

]

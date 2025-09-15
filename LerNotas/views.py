from django.shortcuts import render

# Create your views here.
def SubirNota(request):
    return render(request, 'subir_nota.html')

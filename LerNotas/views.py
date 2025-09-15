from django.shortcuts import render

# Create your views here.
def SubirNota(request):
    return render(request, 'subir_nota.html')

def upload_nota_fiscal(request):
    return render(request, 'upload_nota_fiscal.html')

import os

from django.http import HttpResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET

# Create your views here.
def SubirNota(request):
    # Se o método for POST, significa que o usuário enviou o formulário
    if request.method == 'POST':
        xml_file = request.FILES.get('xml_file')

        # Verificação básica se o arquivo foi enviado e é um XML
        if not xml_file or not xml_file.name.endswith('.xml'):
            contexto_erro = {'erro': 'Por favor, envie um arquivo .xml válido.'}
            return render(request, 'subir_nota.html', contexto_erro)

        try:
            # Para evitar salvar o arquivo em disco, lemos ele diretamente em memória
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # XML de NF-e usa "namespaces". Precisamos disso para encontrar as tags.
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

            # Encontrando o nome do destinatário e o número da nota
            # O .find() busca as tags usando o caminho e o namespace
            nome_cliente_tag = root.find('.//nfe:dest/nfe:xNome', ns)
            numero_nota_tag = root.find('.//nfe:ide/nfe:nNF', ns)

            # Extraindo o texto das tags
            nome_cliente = nome_cliente_tag.text if nome_cliente_tag is not None else "Não encontrado"
            numero_nota = numero_nota_tag.text if numero_nota_tag is not None else "Não encontrado"

            # Criando o contexto para enviar ao novo template
            contexto_resultado = {
                'cliente': nome_cliente,
                'numero_nota': numero_nota
            }

            # Renderiza a página de resultado com os dados extraídos
            return render(request, 'resultado_nota.html', contexto_resultado)

        except ET.ParseError:
            contexto_erro = {'erro': 'Erro ao analisar o XML. Verifique o formato do arquivo.'}
            return render(request, 'subir_nota.html', contexto_erro)

    # Se o método for GET, apenas exibe a página de upload inicial
    return render(request, 'subir_nota.html')

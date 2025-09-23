
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class SubirNotaViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('subir_nota')

    def test_view_get_request(self):
        """
        Teste 1: Verifica se a página de upload carrega corretamente (GET).
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Verificamos se o template correto foi usado para renderizar a página
        self.assertTemplateUsed(response, 'subir_nota.html')

        # Verificamos se um texto chave da página está presente na resposta
        self.assertContains(response, 'Suba aqui sua nota fiscal')

    def test_view_post_valid_xml(self):
        """
        Teste 2: Verifica o envio de um arquivo XML válido.
        """
        # Criamos um conteúdo de XML falso, mas correto.
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
            <NFe>
                <infNFe>
                    <ide>
                        <nNF>12345</nNF>
                    </ide>
                    <dest>
                        <xNome>NOME DO CLIENTE TESTE</xNome>
                    </dest>
                </infNFe>
            </NFe>
        </nfeProc>
        """
        fake_xml_file = SimpleUploadedFile("nota_fiscal.xml", xml_content, content_type="application/xml")

        response = self.client.post(self.url, {'xml_file': fake_xml_file})

        self.assertEqual(response.status_code, 200)

        # Verificamos se, após o sucesso, a página de resultado foi renderizada
        self.assertTemplateUsed(response, 'resultado_nota.html')

        # Verificamos se os dados extraídos estão na página de resultado
        self.assertContains(response, 'NOME DO CLIENTE TESTE')
        self.assertContains(response, '12345')

    def test_view_post_no_file(self):
        """
        Teste 3: Verifica o comportamento ao enviar o formulário sem arquivo.
        """
        # Simula um POST sem dados de arquivo
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 200)

        # Verificamos se ele renderiza a página de upload novamente
        self.assertTemplateUsed(response, 'subir_nota.html')

        # Verificamos se a mensagem de erro correta é exibida
        self.assertContains(response, 'Por favor, envie um arquivo .xml válido.')

    def test_view_post_wrong_file_type(self):
        """
        Teste 4: Verifica o comportamento ao enviar um arquivo que não é XML.
        """
        # Simula o upload de um arquivo .txt
        fake_txt_file = SimpleUploadedFile("nota.txt", b"isso nao e um xml", content_type="text/plain")

        response = self.client.post(self.url, {'xml_file': fake_txt_file})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subir_nota.html')
        self.assertContains(response, 'Por favor, envie um arquivo .xml válido.')

    def test_view_post_malformed_xml(self):
        """
        Teste 5: Verifica o comportamento ao enviar um arquivo XML corrompido.
        """
        # Criamos um conteúdo de XML com uma tag que não fecha
        malformed_xml_content = b"<root><tag>sem fechar"
        malformed_xml_file = SimpleUploadedFile("broken.xml", malformed_xml_content, content_type="application/xml")

        response = self.client.post(self.url, {'xml_file': malformed_xml_file})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subir_nota.html')
        self.assertContains(response, 'Erro ao analisar o XML.')

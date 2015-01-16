import os
import xml.etree.ElementTree as ET

class CarregadorAnotacoes():

    def __init__(self, bd):
        self.bd = bd

    def carrega_anotacao(self, anotador):

        # Diretoria raiz de acordo com o nome do anotador
        diretorio_raiz = anotador + '/Analyses/UAM'

        #Adiciona anotacao no banco de dados
        id_anotacao = self.bd.adiciona_anotacao(anotador)

        # Anda por todas as noticias anotadas
        for subdiretorio in os.walk(diretorio_raiz):

            if subdiretorio[0] == diretorio_raiz:
                continue

            #Abre o arquivo de anotacoes de polaridade no parser de XML
            Noticia_xml = ET.parse(subdiretorio[0] + '/Polaridade.xml')

            #Recupera a raiz do arquivo XML
            raiz = Noticia_xml.getroot()

            #Recupera o nome do arquivo text
            arquivo_txt = raiz[0][0].text

            #Abre o arquivo .txt com a noticica
            try:
                Noticia_texto = open(anotador + '/Corpus/' + arquivo_txt)
            except:
                print subdiretorio[0]
                continue

            #Recupera o texto completo da noticia
            texto_noticia = Noticia_texto.read().decode('utf8')

            #Adiciona noticia ao banco de dado, extraindo as informacoes do xml
            id_noticia = arquivo_txt[arquivo_txt.find('/') + 1:arquivo_txt.find('.')]
            completo = int(raiz[0][2].text[:-1])

            self.bd.adiciona_noticia(id_noticia, id_anotacao, completo)

            #Para cada paragrafo anottado, extrai as informacaores necesarias
            for paragrafo in raiz[1]:

                #Sequencial do paragrafo
                id_paragrafo = int(paragrafo.attrib['id'])

                #inicio e fim de paragrafo
                ini_posic = int(paragrafo.attrib['start'])
                fim_posic = int(paragrafo.attrib['end'])

                #Corta o texto no fonte .txt
                texto_paragrafo = texto_noticia[ini_posic:fim_posic]

                #Polaridade atribuida
                polaridade = paragrafo.attrib['features'][11:]

                if paragrafo.attrib['state'] != 'active':
                    polaridade = ''
                else:
                    if polaridade == 'positivo':
                        polaridade = 'PO'
                    elif polaridade == 'negativo':
                        polaridade = 'NG'
                    elif polaridade == 'neutro':
                        polaridade = 'NE'
                    elif polaridade == 'sem-entidade':
                        polaridade = 'SE'

                #Recupera a entidade definida pelo anotador
                if polaridade in ['NE', 'PO', 'NG']:
                    try:
                        entidade = paragrafo.attrib['comment'].upper()
                    except:
                        print id_noticia, id_paragrafo, texto_paragrafo
                        entidade = ''
                else:
                    entidade = ''

                self.bd.adiciona_paragrafo(id_paragrafo, id_noticia, id_anotacao, texto_paragrafo, ini_posic, fim_posic, polaridade, entidade)

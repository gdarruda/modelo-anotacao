import os
import csv

class ProcessadorCorpus():

    def __init__(self, bd):
        self.bd = bd

    def carrega_lista_noticias(self):

        # Cria conjunto de noticias
        noticias_incluidas = set()

        # Monta dicionario para verificar se determinada noticia eh elegivel
        with open(os.path.join('noticias_incluidas', 'corpus.csv')) as arquivocsv:

            # Transforma em um objeto iteravel
            linhas = csv.reader(arquivocsv, delimiter=';')

            for linha in linhas:

                # Se a linha for 'Incluida', adiciona a colecao
                if linha[1] == 'Incluida':
                    noticias_incluidas.add(int(linha[0]))

        return noticias_incluidas

    def processa_corpus(self):

        # Recuperar as noticias a serem incluidas no corpus
        noticias_incluidas = self.carrega_lista_noticias()

        # Procura todas as noticias extraidas pelo sistema
        cursor_noticias = self.bd.seleciona_noticias_corpus()

        # Percorre todas elas e gera os arquivos textos
        for (id_noticia,) in cursor_noticias:

            # Processa se a noticia for selecionada para geracao do corpus
            if not id_noticia in noticias_incluidas:
                continue

            #Seleciona os paragrafos e sua poalridade
            cursor_polaridade = self.bd.seleciona_polaridade(id_noticia)

            #Variavies de controle do fluxo
            id_paragrafo_atual = 0
            encontrou_maior = True

            #Polaridade das noticias
            for (contador, id_paragrafo, polaridade) in cursor_polaridade:

                #Caso trocou de paragrafo, reinicializa os controladores de fluxo
                if id_paragrafo_atual != id_paragrafo:

                    #Verificar noticias que nao foram incluidas com sucesso
                    if not encontrou_maior:
                        print id_noticia, id_paragrafo

                    #Re-inicializa variaveis de controle
                    encontrou_maior = False
                    id_paragrafo_atual = id_paragrafo

                #Se ainda nao encontro o maior,
                if not encontrou_maior:

                    #Se for maior ou igual a 2, define como polaridade predomeninante
                    if contador >= 2:
                        encontrou_maior = True
                        self.bd.adiciona_noticia_corpus(id_paragrafo, id_noticia, polaridade)


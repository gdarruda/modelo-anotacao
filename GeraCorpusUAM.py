from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import csv

class GeraCorpus(object):

    'Gera o diretorio de corpus para ser utilizado junto ao UAM'

    def __init__(self, bd):
        self.bd = bd
        self.segmentos_gerados = 0

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

    def eh_repeticao(self, id_segmento, matriz_similaridade):

        # Verifica se passa do limiar de similaridade
        for i, similaridade in enumerate(matriz_similaridade[id_segmento]):

            # Se a similaridade for maior que limiar
            if similaridade > 0.8:

                # Gera apenas uma vez segmentos similare
                return i < id_segmento

    def gera_texto(self, dicionario_segmentos, matriz_similaridade):

        # Inicializa variavel texto
        texto = ''

        # Gera o xml para cada noticia
        for id_segmento in dicionario_segmentos:

            # Verifica se eh uma repeticao
            if self.eh_repeticao(id_segmento, matriz_similaridade):
                continue

            # Concatena o texto ao dicionario
            texto = texto + dicionario_segmentos[id_segmento] + '\n'
            self.segmentos_gerados += 1

        # Retorna o texto completo
        return texto

    def gera_noticias(self):

        # Recuperar as noticias a serem incluidas no corpus
        noticias_incluidas = self.carrega_lista_noticias()

        # Procura todas as noticias extraidas pelo sistema
        cursor_noticias = self.bd.seleciona_noticias()

        # Caminho escolhido
        caminho = 'UAM'

        # Lista de segmentos e dicionario de noticias
        lista_segmentos = list()
        dicionario_noticias = dict()

        # Se nao houver o diretorio C1, cria o diretorio
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        # Contador de segmentos
        i = 0

        # Percorre todas elas e gera os arquivos textos
        for (corpo_noticia, id_noticia) in cursor_noticias:

            # Processa se a noticia for selecionada para geracao do corpus
            if not id_noticia in noticias_incluidas:
                continue

            # Separa a noticia em paragrafos
            noticia_segmentada = corpo_noticia.split('\n')

            # Dicionario segmentos
            dicionario_segmentos = dict()

            # Para cada segmento, adiciona na lista para calculo de tf-idf e
            # adiciona nos segmentos da noticia
            for segmento in noticia_segmentada:
                lista_segmentos.append(segmento)
                dicionario_segmentos[i] = segmento
                i += 1

            # Cria um dicionario de noticias
            dicionario_noticias[id_noticia] = dicionario_segmentos

        # Cria a matriz de tf-idf
        tfidf_vectorizer = TfidfVectorizer()
        matriz_tfidf = tfidf_vectorizer.fit_transform(lista_segmentos)
        matriz_similaridade = cosine_similarity(matriz_tfidf, matriz_tfidf)

        # Seleciona os IDs das noticias de forma ordenada
        id_noticias = dicionario_noticias.keys()
        id_noticias.sort(reverse=True)

        # Para cada noticia, gera o arquivo texto
        for id_noticia in id_noticias:

            # Gera o arquivo com o ID da noticia
            arquivo_noticia = open(
                os.path.join(caminho, str(id_noticia) + '.txt'), 'w')
            arquivo_noticia.write(self.gera_texto(
                dicionario_noticias[id_noticia], matriz_similaridade).encode('utf-8'))
            arquivo_noticia.close()

        print 'Segmentos gerados: ' + str(self.segmentos_gerados)

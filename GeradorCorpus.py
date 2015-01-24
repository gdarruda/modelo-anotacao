class GeradorCorpus():

    def __init__(self, bd):
        self.bd = bd

    def seleciona_maioria(self, dicionario):

         valor_maioria = 0
         quantidade_maioria = 0
         chave_maioria = ''

         #Obtem a chave com maior quantidade de votos
         for chave, valor in dicionario.iteritems():

            if valor > valor_maioria:
                valor_maioria = valor
                chave_maioria = chave
                quantidade_maioria = 1
            elif valor == valor_maioria:
                quantidade_maioria+=1

         return (quantidade_maioria, chave_maioria)

    def gera_corpus_ouro(self, id_anotacao_inicio, id_anotacao_fim):

        cursor_paragrafos = self.bd.seleciona_paragrafos_corpus()

        # Percorre todas elas e gera os arquivos textos
        for (id_noticia, id_paragrafo, entidade_minerva, polaridade_minerva) in cursor_paragrafos:

            #Recupera todas as anotacoes de paragrafo no intervalo desejado
            cursor_classificado = self.bd.seleciona_resultados_anotacao(id_noticia, id_paragrafo, id_anotacao_inicio, id_anotacao_fim)

            #Para cada paragrafo, faz o dicionario de polaridades
            dicionario_entidades = dict()
            dicionario_polaridade = dict()

            #Lista de classificaoes/entidades
            lista_classificacao = list()

            #Contabiliza as entidades e polaridades
            for (polaridade, entidade) in cursor_classificado:

                lista_classificacao.append((polaridade, entidade))

                if entidade in dicionario_entidades:
                    dicionario_entidades[entidade] = dicionario_entidades[entidade] + 1
                else:
                    dicionario_entidades[entidade] = 1

            #Caso haja voto de Minerva, adiciona ao conjunto
            if entidade_minerva != None:
                dicionario_entidades[entidade_minerva] = dicionario_entidades[entidade_minerva] + 1

            #Recupera a chave de um dos que obtiveram a maioria e o total de vencedores encontrados
            (total_entidade, entidade_maioria) = self.seleciona_maioria(dicionario_entidades)

            #Nesse caso, nao eh possivel definir a maioria
            if total_entidade > 1:
                print id_noticia, id_paragrafo, str(dicionario_entidades).encode('utf8')
                continue
            else:
                self.bd.atualiza_entidade_paragrafo(id_noticia, id_paragrafo, entidade_maioria)

            # for (polaridade, entidade) in lista_classificacao:
            for (polaridade, entidade) in lista_classificacao:

                # Contabiliza apenas entidade da maioria
                if entidade_maioria == entidade:

                    #Adiciona ao dicionario
                    if polaridade in dicionario_polaridade:
                        dicionario_polaridade[polaridade] = dicionario_polaridade[polaridade] + 1
                    else:
                        dicionario_polaridade[polaridade] = 1

            #Caso haja voto de Minerva, adiciona ao conjunto
            if polaridade_minerva != None:
                # print id_noticia, id_paragrafo
                dicionario_polaridade[polaridade_minerva] = dicionario_polaridade[polaridade_minerva] + 1

            #Recupera a chave de um dos que obtiveram a maioria e o total de vencedores encontrados
            (total_polaridade, polaridade_maioria) = self.seleciona_maioria(dicionario_polaridade)

            # print polaridade_maioria, dicionario_polaridade
            if total_polaridade > 1:
                print id_noticia, id_paragrafo, entidade_maioria.encode('utf8'), str(dicionario_polaridade).encode('utf8')
                continue
            else:
                self.bd.atualiza_polaridade_paragrafo(id_noticia, id_paragrafo, polaridade_maioria)


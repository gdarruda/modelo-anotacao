import os
from lxml import etree

class CorpusXML():

    def __init__(self, bd):
        self.bd = bd
        self.raiz = 'corpus'
        self.caminho_source = os.path.join(self.raiz, 'C1')
        self.caminho_perfis = os.path.join(self.caminho_source, 'sources')
        self.caminho_segmentacao = os.path.join(self.raiz, 'paragraphs')
        self.caminho_segmentador = os.path.join(self.caminho_segmentacao, 'segmenter')
        self.caminho_ouro = os.path.join(self.raiz, 'gold_standard')
        self.caminho_classificacao = os.path.join(self.raiz, 'polarity')
        self.caminho_anotadores = os.path.join(self.caminho_classificacao, 'participants')

    def cria_diretorios(self):

        if not os.path.exists(self.caminho_source):
            os.makedirs(self.caminho_source)

        if not os.path.exists(self.caminho_perfis):
            os.makedirs(self.caminho_perfis)

        if not os.path.exists(self.caminho_segmentacao):
            os.makedirs(self.caminho_segmentacao)

        if not os.path.exists(self.caminho_segmentador):
            os.makedirs(self.caminho_segmentador)

        if not os.path.exists(self.caminho_classificacao):
            os.makedirs(self.caminho_classificacao)

        if not os.path.exists(self.caminho_anotadores):
            os.makedirs(self.caminho_anotadores)

        if not os.path.exists(self.caminho_ouro):
            os.makedirs(self.caminho_ouro)

    def gera_id_documento(self, contador_noticia, prefixo):

        contador_string = str(contador_noticia)

        return prefixo + contador_string.zfill(3)

    def gera_nome_participante(self, id_anotador):

        return 'part_a' + str(id_anotador) + '_parapgraphs_C1.xml'

    def gera_participantes(self):

        for (id_anotador, genero, area, nivel_estudo, idade) in self.bd.seleciona_info_anotadores():

            anotador = etree.Element('plainDocument')
            anotador.append(etree.Element('info', type='id', value='a' + str(id_anotador)))
            anotador.append(etree.Element('info', type='gender', value=genero))
            anotador.append(etree.Element('info', type='age', value=str(idade)))
            anotador.append(etree.Element('info', type='area', value=area))
            anotador.append(etree.Element('info', type='degree', value=nivel_estudo))
            anotador.append(etree.Element('info', type='target-corpus', value='C1'))

            arquivo_anotador = open(os.path.join(self.caminho_anotadores, self.gera_nome_participante(id_anotador)), 'w')
            arquivo_anotador.write(etree.tostring(anotador, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_anotador.close()

    def gera_nome_source(self, id_perfil):

        return 'src_news_' + str(id_perfil) + '_C1.xml'

    def gera_source(self):

        for (id_perfil, nome) in self.bd.seleciona_perfis_twitter():

            perfil = etree.Element('plainDocument')
            perfil.append(etree.Element('info', type='id', value='p' + str(id_perfil)))
            perfil.append(etree.Element('info', type='name', value = nome))
            perfil.append(etree.Element('info', type='target-corpus', value='C1'))

            arquivo_perfil = open(os.path.join(self.caminho_perfis , self.gera_nome_source(id_perfil)), 'w')
            arquivo_perfil.write(etree.tostring(perfil, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_perfil.close()            

    def gera_segmentador(self):

        segmentador = etree.Element('plainDocument')
        segmentador.append(etree.Element('info', type='id', value='s1'))
        segmentador.append(etree.Element('info', type='source', value = 'UAM Corpus Tool'))
        segmentador.append(etree.Element('info', type='url', value='http://www.wagsoft.com/CorpusTool/'))
        segmentador.append(etree.Element('info', type='target-corpus', value='C1'))

        arquivo_segmentador = open(os.path.join(self.caminho_segmentador, 'seg_news_s1_C1.xml'), 'w')
        arquivo_segmentador.write(etree.tostring(segmentador, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        arquivo_segmentador.close()            

    def gera_nome_noticia(self, id_noticia_corpus):

        return 'src_' + id_noticia_corpus + '_C1.xml'

    def gera_noticia(self, seq_noticia, corpo_noticia, perfil):

            id_noticia_corpus = self.gera_id_documento(seq_noticia, 'R')

            noticia = etree.Element('plainDocument')
            noticia.append(etree.Element('info', type='id', value=id_noticia_corpus))
            noticia.append(etree.Element('info', type='corpus', value='C1'))
            noticia.append(etree.Element('info', type='source', value='p' + str(perfil)))

            texto = etree.Element('text')
            texto.text = corpo_noticia
            noticia.append(texto)

            arquivo_noticia = open(os.path.join(self.caminho_source, self.gera_nome_noticia(id_noticia_corpus)), 'w')
            arquivo_noticia.write(etree.tostring(noticia, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_noticia.close()

    def gera_nome_segmentacao(self, seq_segmentacao, seq_noticia):

        return 'seg_' + seq_segmentacao + '_parapgraphs_C1_' + seq_noticia + '_res.xml'

    def gera_segmentacao(self, seq_noticia):

        id_noticia_corpus = self.gera_id_documento(seq_noticia, 'R')
        id_segmentacao = str(seq_noticia).zfill(4)

        nome_arqivo = self.gera_nome_segmentacao(id_segmentacao, id_noticia_corpus)

        segmentacao = etree.Element('plainDocument')
        segmentacao.append(etree.Element('info', type='id', value=id_segmentacao))
        segmentacao.append(etree.Element('info', type='schema', value='paragraphs'))
        segmentacao.append(etree.Element('info', type='source', value=id_noticia_corpus))
        segmentacao.append(etree.Element('info', type='segmenter', value='s1'))
        segmentacao.append(etree.Element('info', type='source-corpus', value='C1'))

        return [segmentacao, nome_arqivo]

    def gera_nome_gold(self, seq_segmentacao, seq_noticia):

        return 'seg_' + seq_segmentacao + '_goldstandard_' + seq_noticia + '_res.xml'

    def gera_gold(self, seq_noticia):

        id_noticia_corpus = self.gera_id_documento(seq_noticia, 'R')
        id_segmentacao = str(seq_noticia).zfill(4)

        nome_arqivo = self.gera_nome_segmentacao(id_segmentacao, id_noticia_corpus)

        segmentacao = etree.Element('plainDocument')
        segmentacao.append(etree.Element('info', type='id', value=id_segmentacao))
        segmentacao.append(etree.Element('info', type='schema', value='goldstandard'))
        segmentacao.append(etree.Element('info', type='source', value=id_noticia_corpus))
        segmentacao.append(etree.Element('info', type='source-corpus', value='C1'))

        return [segmentacao, nome_arqivo]        

    def gera_nome_anotacao(self, id_anotacao, id_segmentacao, id_anotador):
        return 'ann_' + id_anotacao + '_polarity_paragraphs_' + id_segmentacao + '_a' +  id_anotador + '.xml'

    def gera_anotacao(self, seq_anotacao, seq_noticia, id_anotador):

        id_segmentacao = str(seq_noticia).zfill(4)
        id_anotacao = str(seq_anotacao).zfill(4)

        nome_arquivo = self.gera_nome_anotacao(id_anotacao, id_segmentacao, str(id_anotador))

        anotacao = etree.Element('plainDocument')
        anotacao.append(etree.Element('info', type='id', value=id_anotacao))
        anotacao.append(etree.Element('info', type='schema', value='polarity'))
        anotacao.append(etree.Element('info', type='annotator', value='a' + str(id_anotador)))
        anotacao.append(etree.Element('info', type='source', value=id_segmentacao))
        anotacao.append(etree.Element('info', type='source-corpus', value='paragraphs'))

        return [anotacao, nome_arquivo]

    def gera_corpus(self):

        self.cria_diretorios()
        self.gera_participantes()
        self.gera_source()
        self.gera_segmentador()

        seq_noticia = 1
        seq_paragrafo = 1
        seq_anotacao = 1

        anotacoes = {1:40, 2:41 , 3:42, 4:44};

        for (id_noticia, corpo, perfil) in self.bd.seleciona_noticia_corpus():

            self.gera_noticia(seq_noticia, corpo, perfil)

            segmentacao = self.gera_segmentacao(seq_noticia)
            gold_standard = self.gera_gold(seq_noticia)

            anotacoes_paragrafo = {}

            for (id_paragrafo, paragrafo, polaridade_ouro, entidade_ouro) in self.bd.seleciona_paragrafo_noticia(id_noticia):

                segmento = etree.Element('unit', id=str(seq_paragrafo).zfill(4))

                texto_paragrafo = etree.Element('text')
                texto_paragrafo.text = paragrafo
                segmento.append(texto_paragrafo)

                gold_annotation = etree.Element('unit', id=str(seq_paragrafo).zfill(4))
                gold_annotation.append(etree.Element('ann', type='polarity', value=polaridade_ouro))
                gold_annotation.append(etree.Element('ann', type='entity', value=entidade_ouro))

                segmentacao[0].append(segmento)
                gold_standard[0].append(gold_annotation)                

                for id_anotador, id_anotacao in anotacoes.iteritems():

                    if id_anotador not in anotacoes_paragrafo:
                        anotacoes_paragrafo[id_anotador] = self.gera_anotacao(seq_anotacao, seq_noticia, id_anotador)
                        seq_anotacao+=1

                    for (polaridade, entidade) in self.bd.seleciona_resultados_anotacao(id_noticia, id_paragrafo, id_anotacao, id_anotacao):

                        paragrafo = etree.Element('mark', unit=str(seq_paragrafo).zfill(4))
                        paragrafo.append(etree.Element('ann', type='polarity', value=polaridade))
                        paragrafo.append(etree.Element('ann', type='entity', value=entidade))
                        anotacoes_paragrafo[id_anotador][0].append(paragrafo)

                seq_paragrafo+=1

            arquivo_segmentacao = open(os.path.join(self.caminho_segmentacao, segmentacao[1]),'w')
            arquivo_segmentacao.write(etree.tostring(segmentacao[0], pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_segmentacao.close()

            arquivo_gold_standard = open(os.path.join(self.caminho_ouro, gold_standard[1]),'w')
            arquivo_gold_standard.write(etree.tostring(gold_standard[0], pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_gold_standard.close()

            for id_anotador, anotacao in anotacoes_paragrafo.iteritems():

                arquivo_anotacao = open(os.path.join(self.caminho_classificacao, anotacao[1]),'w')
                arquivo_anotacao.write(etree.tostring(anotacao[0], pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                arquivo_anotacao.close()

            seq_noticia+=1

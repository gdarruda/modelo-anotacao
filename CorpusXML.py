import os
from lxml import etree

class CorpusXML():

    def __init__(self, bd):
        self.bd = bd
        self.raiz = 'corpus'
        self.caminho_source = os.path.join(self.raiz, 'C1')
        self.caminho_segmentacao =  os.path.join(self.raiz, 'paragraphs')
        self.caminho_classificacao = os.path.join(self.raiz, 'polarity')
        self.caminho_anotadores = os.path.join(self.caminho_source, 'participants')

    def cria_diretorios(self):

        if not os.path.exists(self.caminho_source):
                os.makedirs(self.caminho_source)

        if not os.path.exists(self.caminho_segmentacao):
                os.makedirs(self.caminho_segmentacao)

        if not os.path.exists(self.caminho_classificacao):
                os.makedirs(self.caminho_classificacao)

        if not os.path.exists(self.caminho_anotadores):
                os.makedirs(self.caminho_anotadores)

    def gera_id_documento(self, contador_noticia, prefixo):

        contador_string = str(contador_noticia)

        return prefixo + contador_string.zfill(3)

    def gera_nome_participante(self, id_anotador):

        return 'part_a' + str(id_anotador) + '_C1.xml'

    def gera_participantes(self):

        for (id_anotador, genero, area, nivel_estudo) in self.bd.seleciona_info_anotadores():

            anotador = etree.Element('plainDocument')
            anotador.append(etree.Element('info', type='id', value='a' + str(id_anotador)))
            anotador.append(etree.Element('info', type='gender', value=genero))
            anotador.append(etree.Element('info', type='area', value=area))
            anotador.append(etree.Element('info', type='degree', value=nivel_estudo))
            anotador.append(etree.Element('info', type='target-corpus', value='C1'))

            arquivo_anotador = open(os.path.join(self.caminho_anotadores, self.gera_nome_participante(id_anotador)), 'w')
            arquivo_anotador.write(etree.tostring(anotador, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_anotador.close()

    def gera_nome_noticia(self, id_noticia_corpus):

        return 'src_' + id_noticia_corpus + '_C1.xml'

    def gera_noticia(self, seq_noticia, corpo_noticia, perfil):

            id_noticia_corpus = self.gera_id_documento(seq_noticia, 'R')

            noticia = etree.Element('plainDocument')
            noticia.append(etree.Element('info', type='id', value=id_noticia_corpus))
            noticia.append(etree.Element('info', type='corpus', value='C1'))
            noticia.append(etree.Element('info', type='source', value=perfil))

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
        segmentacao.append(etree.Element('info', type='source-corpus', value='C1'))

        return [segmentacao, nome_arqivo]

    def gera_nome_anotacao(self, seq_segmentacao, id_anotador):
        return 'ann_' + seq_segmentacao + '_polarity_paragraphs_' + seq_segmentacao + '_a' +  id_anotador + '.xml'

    def gera_anotacao(self, seq_paragrafo, seq_noticia, id_anotador):

        id_segmentacao = str(seq_noticia).zfill(4)

        nome_arquivo = self.gera_nome_anotacao(id_segmentacao, str(id_anotador))

        anotacao = etree.Element('plainDocument')
        anotacao.append(etree.Element('info', type='id', value=id_segmentacao))
        anotacao.append(etree.Element('info', type='schema', value='polarity'))
        anotacao.append(etree.Element('info', type='annotator', value='a' + str(id_anotador)))
        anotacao.append(etree.Element('info', type='source', value=id_segmentacao))
        anotacao.append(etree.Element('info', type='source-corpus', value='paragraphs'))

        return [anotacao, nome_arquivo]

    def gera_corpus(self):

        self.cria_diretorios()
        self.gera_participantes()

        seq_noticia = 1
        seq_paragrafo = 1

        anotacoes = {1:40, 2:41 , 3:42, 4:44};

        for (id_noticia, corpo, perfil) in self.bd.seleciona_noticia_corpus():

            self.gera_noticia(seq_noticia, corpo, perfil)

            segmentacao = self.gera_segmentacao(seq_noticia)

            anotacoes_paragrafo = {}

            for (id_paragrafo, paragrafo) in self.bd.seleciona_paragrafo_noticia(id_noticia):

                segmento = etree.Element('unit', id=str(seq_paragrafo).zfill(4))
                segmento.text = paragrafo
                segmentacao[0].append(segmento)

                for id_anotador, id_anotacao in anotacoes.iteritems():

                    if id_anotador not in anotacoes_paragrafo:
                        anotacoes_paragrafo[id_anotador] = self.gera_anotacao(seq_paragrafo, seq_noticia, id_anotador)

                    for (polaridade, entidade) in self.bd.seleciona_resultados_anotacao(id_noticia, id_paragrafo, id_anotacao, id_anotacao):

                        paragrafo = etree.Element('mark', unit=str(seq_paragrafo).zfill(4))
                        paragrafo.append(etree.Element('ann', type='polarity', value=polaridade))
                        paragrafo.append(etree.Element('ann', type='entity', value=entidade))
                        anotacoes_paragrafo[id_anotador][0].append(paragrafo)

                seq_paragrafo+=1

            arquivo_segmentacao = open(os.path.join(self.caminho_segmentacao, segmentacao[1]),'w')
            arquivo_segmentacao.write(etree.tostring(segmentacao[0], pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_segmentacao.close()

            for id_anotador, anotacao in anotacoes_paragrafo.iteritems():

                arquivo_anotacao = open(os.path.join(self.caminho_classificacao, anotacao[1]),'w')
                arquivo_anotacao.write(etree.tostring(anotacao[0], pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                arquivo_anotacao.close()

            seq_noticia+=1

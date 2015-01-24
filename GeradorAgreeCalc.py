from lxml import etree
import os

class GeradorAgreeCalc():

    def __init__(self, bd):
        self.bd = bd

    def gera_nome_anotador(self, id_anotacao):

        contador_anotador = str(id_anotacao)

        return 'part_a' + contador_anotador.zfill(2) + '_polaridade.xml'

    def gera_nome_noticia(self, id_sequencial_noticia, id_anotacao, id_noticia):

        contador_sequencial = str(id_sequencial_noticia)
        contador_noticia = str(id_noticia)
        contador_anotacao = str(id_anotacao)

        return 'ann_' + contador_sequencial.zfill(4) + '_polaridade_noticia_' + contador_noticia.zfill(4) + '_a' + contador_anotacao.zfill(2) + '.xml'

    def gera_anotacao(self, id_anotacao_inicial, id_anotacao_final):

        #Caminho do corpus
        diretorio = 'polaridade'

        #Se nao houver o diretorio do corpu, cria.
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        #Processa todos os anotadores
        cursor_anotadores = self.bd.seleciona_anotadores(id_anotacao_inicial, id_anotacao_final)

        #Caminho das informacoes dos anotadores
        subdir_anotadores = 'participants'

        #Sequencial de noticias
        id_sequencial_noticia = 1

        #Para cada anotador, gera o documento do anotador
        for (id_anotacao, nome) in cursor_anotadores:

            #Sequencial de numero dos paragrafos
            id_sequencial_paragrafo = 1

            # Cria o XML do anotador
            anotador = etree.Element('plainDocument')

            #Adiciona informacoes basicas dos anotadores
            anotador.append(etree.Element('info', type='id', value='a' + str(id_anotacao)))
            anotador.append(etree.Element('target-corpus', type='polaridade'))

            #Monta o diretorio completo
            full_dir = os.path.join(diretorio, subdir_anotadores)

            #Se nao houver o diretorio, cria.
            if not os.path.exists(full_dir):
                os.makedirs(full_dir)

            #Cria o arquivo do anotador e imprime o xml
            arquivo_anotador = open(os.path.join(full_dir, self.gera_nome_anotador(id_anotacao)), 'w')
            arquivo_anotador.write(etree.tostring(anotador, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
            arquivo_anotador.close()

            cursor_noticias = self.bd.seleciona_noticias(id_anotacao)

            #Para cada noticia classificada pelo anotador...
            for (id_noticia,) in cursor_noticias:

                #Cria o XML da noticia
                noticia = etree.Element('annotation')

                #Adiciona informacoes de cabecalho
                noticia.append(etree.Element('info', type='id', value=str(id_sequencial_noticia)))
                noticia.append(etree.Element('info', type='scheme', value='polaridade'))
                noticia.append(etree.Element('info', type='annotator', value= 'a' + str(id_anotacao)))
                noticia.append(etree.Element('info', type='source', value=str(id_noticia)))
                noticia.append(etree.Element('info', type='source-corpus', value='noticias'))

                cursor_paragrafos = self.bd.seleciona_paragrafos(id_anotacao, id_noticia)

                #Para cada paragrafo...
                for (polaridade,entidade) in cursor_paragrafos:

                    paragrafo = etree.Element('mark',unit=str(id_sequencial_paragrafo))
                    paragrafo.append(etree.Element('ann', value=polaridade, type='polaridade'))
                    paragrafo.append(etree.Element('ann', value=entidade, type='entidade'))
                    noticia.append(paragrafo)

                    #Adiciona uma ao contador de paragrafos
                    id_sequencial_paragrafo += 1

                arquivo_noticia = open(os.path.join(diretorio, self.gera_nome_noticia(id_sequencial_noticia, id_anotacao, id_noticia)),'w')
                arquivo_noticia.write(etree.tostring(noticia, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                arquivo_noticia.close()

                #Adiciona um ao contador de noticias
                id_sequencial_noticia += 1





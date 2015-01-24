import mysql.connector


class BancoMySQL():

    'Classe para manipulacao de banco de dados em MySQL'

    def __init__(self, usuario, senha, host, banco):
        self.conexao = mysql.connector.connect(user=usuario, password=senha, host=host, database=banco, buffered=True)

    def adiciona_anotacao(self, nome):

        cursor_anotacao = self.conexao.cursor()

        insert_anotacao = ('insert into anotacoes (nome) values (%s)')
        cursor_anotacao.execute(insert_anotacao, (nome,))

        self.conexao.commit()

        return cursor_anotacao.lastrowid

    def adiciona_noticia(self, id_noticia, id_anotacao, completo):

        cursor_noticia = self.conexao.cursor()

        insert_noticia = ('insert into noticias_x_anotacao values (%s, %s, %s)')
        dados_noticia = (id_noticia, id_anotacao, completo)

        cursor_noticia.execute(insert_noticia, dados_noticia)

        self.conexao.commit()

    def adiciona_paragrafo(self, id_paragrafo, id_noticia, id_anotacao, paragrafo, ini_posic, fim_posic, polaridade, entidade):

        cursor_paragrafo = self.conexao.cursor()

        insert_paragrafo = ('insert into noticias_x_anotacao_x_paragrafo values (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
        dados_paragrafo = (id_paragrafo, id_noticia, id_anotacao, paragrafo, ini_posic, fim_posic, polaridade, entidade, entidade)

        cursor_paragrafo.execute(insert_paragrafo, dados_paragrafo)

        self.conexao.commit()

    def seleciona_anotadores(self, id_anotacao_inicial, id_anotacao_final):

        cursor_anotadores = self.conexao.cursor()

        query_noticia = ('select id_anotacao, nome from anotacoes where id_anotacao between %s and %s')
        filtro_anotacao = (id_anotacao_inicial, id_anotacao_final)

        cursor_anotadores.execute(query_noticia, filtro_anotacao)

        return cursor_anotadores

    def seleciona_paragrafos_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        query_noticias = ('select n.id_noticia, np.id_paragrafo, np.entidade_minerva, np.polaridade_minerva from noticias n join noticias_x_paragrafo np on np.id_noticia = n.id_noticia where n.ind_corpus = \'S\'')
        cursor_paragrafos.execute(query_noticias)

        return cursor_paragrafos

    def seleciona_resultados_anotacao(self, id_noticia, id_paragrafo, id_anotacao_inicial, id_anotacao_final):

        cursor_anotacao = self.conexao.cursor()

        query_paragrafos = ('select polaridade, entidade_normalizada from noticias_x_anotacao_x_paragrafo where id_anotacao between %s and %s and id_noticia = %s and id_paragrafo = %s')
        cursor_anotacao.execute(query_paragrafos, (id_anotacao_inicial,id_anotacao_final, id_noticia, id_paragrafo))

        return cursor_anotacao

    def atualiza_entidade_paragrafo(self, id_noticia, id_paragrafo, entidade):

        cursor_entidade = self.conexao.cursor()

        updata_anotador = ('update noticias_x_paragrafo set entidade = %s where id_noticia = %s and id_paragrafo = %s')
        cursor_entidade.execute(updata_anotador,(entidade, id_noticia, id_paragrafo))

        self.conexao.commit()

    def atualiza_polaridade_paragrafo(self, id_noticia, id_paragrafo, polaridade):

        cursor_polaridade = self.conexao.cursor()

        updata_anotador = ('update noticias_x_paragrafo set polaridade = %s where id_noticia = %s and id_paragrafo = %s')
        cursor_polaridade.execute(updata_anotador,(polaridade, id_noticia, id_paragrafo))

        self.conexao.commit()

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

        insert_paragrafo = ('insert into noticias_x_paragrafo values (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
        dados_paragrafo = (id_paragrafo, id_noticia, id_anotacao, paragrafo, ini_posic, fim_posic, polaridade, entidade, entidade)

        cursor_paragrafo.execute(insert_paragrafo, dados_paragrafo)

        self.conexao.commit()

    def seleciona_anotadores(self):

        cursor_anotadores = self.conexao.cursor()

        query_noticia = ('select id_anotacao, nome from anotacoes')
        cursor_anotadores.execute(query_noticia)

        return cursor_anotadores

    def seleciona_noticias_corpus(self):

        cursor_noticias = self.conexao.cursor()

        query_noticias = ('select id_noticia from noticias where corpo != \'\' order by id_noticia desc')
        cursor_noticias.execute(query_noticias)

        return cursor_noticias

    def seleciona_noticias(self, id_anotacao):

        cursor_anotadores = self.conexao.cursor()

        query_noticia = ('select id_noticia from noticias_x_anotacao where id_anotacao = %s')
        cursor_anotadores.execute(query_noticia,(id_anotacao,))

        return cursor_anotadores

    def seleciona_paragrafos(self, id_anotacao, id_noticia):

        cursor_paragrafo = self.conexao.cursor()

        query_noticia = ('select replace(polaridade,\'SE\',\'\') polaridade from noticias_x_paragrafo where id_anotacao = %s and id_noticia = %s  order by id_paragrafo')
        cursor_paragrafo.execute(query_noticia,(id_anotacao,id_noticia))

        return cursor_paragrafo

    def adiciona_noticia_corpus(self, id_paragrafo, id_noticia, polaridade):

        cursor_noticia = self.conexao.cursor()

        insert_noticia = ('insert into noticias_corpus (id_noticia, id_paragrafo, polaridade) VALUES (%s, %s, %s)')
        dados_noticia = (id_noticia, id_paragrafo, polaridade)

        cursor_noticia.execute(insert_noticia, dados_noticia)

        self.conexao.commit()

    def seleciona_polaridade(self, id_noticia):

        cursor_polaridade = self.conexao.cursor()

        query_polaridade = ('select count(*) contador, id_paragrafo, IF(char_length(polaridade)>0, polaridade,\'NC\') polaridade ' +
                            'from noticias_x_paragrafo ncp ' +
                            'where id_noticia = %s ' +
                            'group by id_paragrafo, IF(char_length(polaridade)>0, polaridade,\'NC\') ' +
                            'order by id_paragrafo')

        cursor_polaridade.execute(query_polaridade,(id_noticia,))

        return cursor_polaridade


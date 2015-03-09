from BancoDados import BancoMySQL
from GeradorAgreeCalc import GeradorAgreeCalc
from CarregadorAnotacaoes import CarregadorAnotacoes
from GeraCorpusUAM import GeraCorpus

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def carrega_anotacoes():

    CG = CarregadorAnotacoes(bd)
    # CG.carrega_anotacao('Henrique')
    # CG.carrega_anotacao('Natasha')
    # CG.carrega_anotacao('Victor')
    # CG.carrega_anotacao('Bonacin')
    CG.carrega_anotacao('NatashaComplemento')

def gera_corpus_anotado(id_anotacao_inicial, id_anotacao_final, padraoOuro):

    GAC = GeradorAgreeCalc(bd)
    GAC.gera_anotacao(id_anotacao_inicial, id_anotacao_final, padraoOuro)

def gerador_corpus_ouro(id_anotacao_inicial, id_anotacao_final):

    GC = GeradorCorpus(bd)
    GC.gera_corpus_ouro(id_anotacao_inicial, id_anotacao_final)

def gera_noticias():
    GC = GeraCorpus(bd)
    GC.gera_noticias()

# gerador_corpus_ouro(40,44)
gera_corpus_anotado(40,40,False)
# gera_noticias()
# carrega_anotacoes()

from BancoDados import BancoMySQL
from GeradorAgreeCalc import GeradorAgreeCalc
from CarregadorAnotacaoes import CarregadorAnotacoes

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')


def carrega_anotacoes():

    CG = CarregadorAnotacoes(bd)
    CG.carrega_anotacao('Victor')


def gera_corpus_anotado():

    GAC = GeradorAgreeCalc(bd)
    GAC.gera_anotacao()

gera_corpus_anotado()

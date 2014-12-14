from BancoDados import BancoMySQL
from GeradorAgreeCalc import GeradorAgreeCalc
from CarregadorAnotacaoes import CarregadorAnotacoes
from ProcessadorCorpus import ProcessadorCorpus

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')


def carrega_anotacoes():

    CG = CarregadorAnotacoes(bd)
    CG.carrega_anotacao('Bonacin')

def gera_corpus_anotado():

    GAC = GeradorAgreeCalc(bd)
    GAC.gera_anotacao()

def processa_corpus():

    PC = ProcessadorCorpus(bd)
    PC.processa_corpus()

processa_corpus()

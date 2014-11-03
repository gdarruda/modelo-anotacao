from BancoDados import BancoMySQL
from CarregadorAnotacaoes import CarregadorAnotacoes

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')


def carrega_anotacoes():

    CG = CarregadorAnotacoes(bd)
    CG.carrega_anotacao('Natasha')

carrega_anotacoes()

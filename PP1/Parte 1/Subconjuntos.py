class Subconjuntos(object):
    def __init__(self, pontos):
        self.pontos = pontos
        self.suporte = [pontos[3],pontos[0]]
        self.nucleo = [pontos[2],pontos[1]]
        self.selecionado = False

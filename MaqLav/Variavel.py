class Variavel(object):
    def __init__(self, conjuntos):
        self.conj=conjuntos
        self.conj_selecionado=0

    def get_pert(self, ponto):
        return self.conj[self.conj_selecionado].get_pert(ponto)

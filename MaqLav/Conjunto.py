import numpy as np

class Conjunto(object):
    def __init__(self, pontos, nome):
        self.pontos = pontos #Lista de listas(X,Y)
        self.nome = nome
        self.selecionado = False

    def get_pert(self, ponto):
        #Se antes do primeiro ponto, retorna a pertinência do primeiro
        if ponto <= self.pontos[0][0]:
            return self.pontos[0][1]
        #Se depois do último ponto, retorna a pertinência do último
        if ponto >= self.pontos[-1][0]:
            return self.pontos[-1][1]

        #Encontra o intervalo onde o ponto desejado esta incluído
        i=0
        while ponto > self.pontos[i][0]:
            i+=1
        
        razao=(ponto - self.pontos[i-1][0])/(self.pontos[i][0] - self.pontos[i-1][0])
        if self.pontos[i][1] < self.pontos[i-1][1]:
            razao = 1 - razao

        #Ponto mínimo + (diferença dos dois pontos * razao)
        return min(self.pontos[i][1], self.pontos[i-1][1]) + abs(self.pontos[i][1] - self.pontos[i-1][1])*razao

    def get_height(self):
        return max(np.array(self.pontos)[:,1])
        

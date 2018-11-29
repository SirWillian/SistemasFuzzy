#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
from Conjunto import Conjunto

def negacao(conj):
    #Negacao por complemento
    conj_out=copy.deepcopy(conj)
    for i in range(len(conj.pontos)):
        conj_out.pontos[i][1] = 1 - conj.pontos[i][1]
    return conj_out

def muito(conj, crescente):
    #Intensifica um conjunto deslocando-o
    deslocamento = (conj.pontos[-1][0] - conj.pontos[0][0])/2
    conj_out=copy.deepcopy(conj)
    for i in range(len(conj.pontos)):
        if(crescente):
            conj_out.pontos[i][0]+=deslocamento
        else:
            conj_out.pontos[i][0]-=deslocamento
    return conj_out
    
def uniao(conj_a, conj_b):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=10, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=10, endpoint=True)

    discreto=np.unique(np.concatenate((discreto_a, discreto_b)))

    #Itera em todos os pontos e monta o conjunto de saida
    conj_out=Conjunto([],"uniao (" + conj_a.nome + conj_b.nome + ")")
    for point in discreto:
        if conj_a.get_pert(point) > conj_b.get_pert(point):
            conj_out.pontos.append((point, conj_a.get_pert(point)))
        else:
            conj_out.pontos.append((point, conj_b.get_pert(point)))

    return conj_out

def intersecao(conj_a, conj_b):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=10, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=10, endpoint=True)

    discreto=np.unique(np.concatenate((discreto_a, discreto_b)))

    #Itera em todos os pontos e monta o conjunto de saida
    conj_out=Conjunto([],"intersecao (" + conj_a.nome + conj_b.nome + ")")
    for point in discreto:
        if conj_a.get_pert(point) < conj_b.get_pert(point):
            conj_out.pontos.append((point, conj_a.get_pert(point)))
        else:
            conj_out.pontos.append((point, conj_b.get_pert(point)))

    return conj_out

def conjuncao(conj_a, conj_b, n_steps, tipo):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=n_steps, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=n_steps, endpoint=True)

    #Para cada ponto de cada grupo, calcula norma-t
    output=[]
    for x in discreto_a:
        for y in discreto_b:
            #Regra de Mamdani
            if(tipo==0):
                output.append((x,y,min(conj_a.get_pert(x),conj_b.get_pert(y))))
            #Regra de Lassen
            else:
                output.append((x,y,conj_a.get_pert(x)*conj_b.get_pert(y)))
    return output

def disjuncao(conj_a, conj_b, n_steps):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=n_steps, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=n_steps, endpoint=True)

    #Para cada ponto de cada grupo, calcula norma-s
    output=[]
    for x in discreto_a:
        for y in discreto_b:
            output.append((x,y,max(conj_a.get_pert(x),conj_b.get_pert(y))))
    return output

def implicacao(conj_a,conj_b,n_steps,tipo):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=n_steps, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=n_steps, endpoint=True)

    #Para cada ponto de cada grupo, calcula a implicação
    output=[]
    for x in discreto_a:
        for y in discreto_b:
            if(tipo=="s"):
                output.append((x,y,max(negacao(conj_a).get_pert(x),conj_b.get_pert(y))))
            elif(tipo=="luca"):
                output.append((x,y,min(1,1-min(conj_a.get_pert(x),conj_b.get_pert(y)))))
            elif(tipo=="godel"):
                if(conj_a.get_pert(x)<=conj_b.get_pert(y)):
                    output.append((x,y,1))
                else:
                    output.append((x,y,conj_b.get_pert(y)))
            elif(tipo=="kleene"):
                output.append((x,y,max(1-conj_a.get_pert(x),conj_b.get_pert(y))))
            elif(tipo=="zadeh"):
                output.append((x,y,max(1-conj_a.get_pert(x),min(conj_a.get_pert(x),conj_b.get_pert(y)))))
    return output

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
from Conjunto import Conjunto

def negacao(conj):
    #Negacao por complemento
    conj_out=copy.deepcopy(conj)
    conj_out.nome = "nao " + conj.nome
    for i in range(len(conj.pontos)):
        conj_out.pontos[i][1] = 1 - conj.pontos[i][1]
    return conj_out

def normalizacao(conj):
    altura=conj.get_height()
    conj_out=copy.deepcopy(conj)
    for i in range(len(conj.pontos)):
        conj_out.pontos[i][1] = conj.pontos[i][1]/altura
    return conj_out

def levemente(conj, n_steps):
    #Normalização de (u(x) E não muito u(x))
    discreto = np.linspace(conj.pontos[0][0], conj.pontos[-1][0], num=n_steps, endpoint=True)
    conj_out = Conjunto([],"levemente "+conj.nome)
    conj_nao_muito = negacao(muito(conj,n_steps))
    for x in discreto:
        conj_out.pontos.append([x,min(conj.get_pert(x), conj_nao_muito.get_pert(x))])
    conj_out = normalizacao(conj_out)
    return conj_out

def muito(conj, n_steps):
    #Pertinência de cada ponto ao quadrado
    discreto = np.linspace(conj.pontos[0][0], conj.pontos[-1][0], num=n_steps, endpoint=True)
    conj_out=Conjunto([],"muito "+conj.nome)
    for x in discreto:
        conj_out.pontos.append([x,conj.get_pert(x)**2])
    return conj_out
    
def uniao(conj_a, conj_b, n_steps):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=n_steps, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=n_steps, endpoint=True)

    discreto=np.unique(np.concatenate((discreto_a, discreto_b)))

    #Itera em todos os pontos e monta o conjunto de saida
    conj_out=Conjunto([],"uniao (" + conj_a.nome + conj_b.nome + ")")
    for point in discreto:
        if conj_a.get_pert(point) > conj_b.get_pert(point):
            conj_out.pontos.append([point, conj_a.get_pert(point)])
        else:
            conj_out.pontos.append([point, conj_b.get_pert(point)])

    return conj_out

def intersecao(conj_a, conj_b, n_steps):
    #Pega uma distribuição de pontos
    discreto_a = np.linspace(conj_a.pontos[0][0], conj_a.pontos[-1][0], num=n_steps, endpoint=True)
    discreto_b = np.linspace(conj_b.pontos[0][0], conj_b.pontos[-1][0], num=n_steps, endpoint=True)

    discreto=np.unique(np.concatenate((discreto_a, discreto_b)))

    #Itera em todos os pontos e monta o conjunto de saida
    conj_out=Conjunto([],"intersecao (" + conj_a.nome + conj_b.nome + ")")
    for point in discreto:
        if conj_a.get_pert(point) < conj_b.get_pert(point):
            conj_out.pontos.append([point, conj_a.get_pert(point)])
        else:
            conj_out.pontos.append([point, conj_b.get_pert(point)])

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

def inferencia_mamdani(antecedentes, consequente, entradas, n_steps):
    conj_out=Conjunto([],"inferencia ")
    pertinencias=[]
    #Matching (min ou prod, para singletons, é o mesmo que o valor no ponto)
    for i in range(len(entradas)):
        pertinencias.append(antecedentes[i].get_pert(entradas[i]))
        conj_out.nome+=(" E " + antecedentes[i].nome)

    #Agregação dos antecedentes
    agregacao=np.min(pertinencias)

    #Inferencia (min)
    discreto_consequente = np.linspace(consequente.pontos[0][0], consequente.pontos[-1][0], num=n_steps, endpoint=True)
    conj_out.pontos=[(discreto_consequente[i],min(agregacao,consequente.get_pert(discreto_consequente[i]))) for i in range(len(discreto_consequente))]

    return conj_out

def inferencia_sugeno(antecedentes, entradas, n_steps):
    pertinencias=[]
    #Matching (min ou prod, para singletons, é o mesmo que o valor no ponto)
    for i in range(len(entradas)):
        pertinencias.append(antecedentes[i].get_pert(entradas[i]))

    #Grau de ativação da regra
    ativacao=np.min(pertinencias)

    return ativacao

def defuzzificacao(conj, metodo, n_steps):
    discreto = np.linspace(conj.pontos[0][0], conj.pontos[-1][0], num=n_steps, endpoint=True)

    numerador=0
    denominador=0

    #Método CoG
    for x in discreto:
        numerador += x*conj.get_pert(x)
        denominador += conj.get_pert(x)

    defuzzy = numerador/denominador
    return defuzzy

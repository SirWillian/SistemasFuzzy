#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
from Conjunto import Conjunto

def regra(antecedente, consequente, n_steps):
    discreto_c = np.linspace(consequente.pontos[0][0], consequente.pontos[-1][0], num=n_steps, endpoint=True)

    output=[]
    #Semantica padrão: min    
    for ponto in antecedente:
        for x in discreto_c:
            output.append(tuple(list(ponto)[:len(ponto)-1]) + (x,min(ponto[-1],consequente.get_pert(x))))

    return np.array(output)

def expansao_cilindrica(relacao, limites, n_steps):
    discreto_limites = np.linspace(limites[0], limites[1], num=n_steps, endpoint=True)

    output=[]
    for ponto in relacao:
        for l in discreto_limites:
            output.append(tuple(list(ponto)[:len(ponto)-1]) + (l,ponto[-1]))

    return np.array(output)

def projecao(relacao, eixo):
    #Verifica se é um eixo projetável
    if(eixo>len(relacao[0])-2):
        print("Eixo não existente")
    else:
        valores_eixo=sorted(set(relacao[:,eixo]))
        output=[]
        for valor in valores_eixo:
            pontos_relacao=relacao[relacao[:,eixo]==valor]
            output.append((valor,np.max(pontos_relacao[:,-1])))

    return Conjunto(output,"projecao")

def uniao(rel_a, rel_b):
    output=[]
    for i in range(len(rel_a)):
        output.append(tuple(list(rel_a[i])[:len(rel_a[i])-1]) + (max(rel_a[i][-1],rel_b[i][-1]),))

    return np.array(output)

def intersecao(rel_a, rel_b):
    output=[]
    for i in range(len(rel_a)):
        output.append(tuple(list(rel_a[i])[:len(rel_a[i])-1]) + (min(rel_a[i][-1],rel_b[i][-1]),))

    return np.array(output)
                        



#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conjunto import Conjunto
from Variavel import Variavel
from Regra import Regra
import ConjuntoOperator as co
import RelacaoOperator as ro

from mpl_toolkits import mplot3d
from matplotlib import cm
import numpy as np
import itertools
import matplotlib.pyplot as plt
import sys

def surface_plot(regra):
    fig=plt.figure()
    ax=plt.axes(projection="3d")
    
    x=np.unique(np.array(regra)[:,0])
    y=np.unique(np.array(regra)[:,1])
    X,Y = np.meshgrid(x,y)
    zs=np.array(regra)[:,2]
    Z=zs.reshape(X.shape)

    surf=ax.plot_surface(X,Y,Z,rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0)
    fig.colorbar(surf,shrink=0.5,aspect=5)
    plt.show()

def conj_plot(conj):
    plt.plot(np.array(conj.pontos)[:,0],np.array(conj.pontos)[:,1])
    plt.show()

def rule_bank_plot(regras, entrada):
    fig, ax = plt.subplots(len(regras), len(regras[0].antecedentes)+1, sharex='col', sharey='row')
    fig.subplots_adjust(hspace=0.2, wspace=0.4)
    fig.suptitle('Banco de regras', fontsize=16)
    for i in range(len(regras)):
        for j in range(len(regras[i].antecedentes)):
            ax[i,j].fill_between(np.array(regras[i].antecedentes[j].pontos)[:,0],np.array(regras[i].antecedentes[j].pontos)[:,1], alpha=0.5)
        ax[i,len(regras[i].antecedentes)].fill_between(np.array(regras[i].consequente.pontos)[:,0],np.array(regras[i].consequente.pontos)[:,1], alpha=0.5, color='r')
    plt.show()

sujeira = Variavel([Conjunto([[0,1],[50,0],[100,0]],"PS"),Conjunto([[0,0],[50,1],[100,0]],"MS"),Conjunto([[0,0],[50,0],[100,1]],"GS")])
manchas = Variavel([Conjunto([[0,1],[50,0],[100,0]],"PM"),Conjunto([[0,0],[50,1],[100,0]],"MM"),Conjunto([[0,0],[50,0],[100,1]],"GM")])
tempo = Variavel([Conjunto([[0,1],[10,0],[60,0]],"MC"),Conjunto([[0,0],[10,1],[25,0],[60,0]],"C"),Conjunto([[0,0],[10,0],[25,1],[40,0],[60,0]],"M"),Conjunto([[0,0],[25,0],[40,1],[60,0]],"L"),Conjunto([[0,0],[40,0],[60,1]],"ML")])

regras_mamdani=[]
regras_mamdani.append(Regra([sujeira.conj[0],manchas.conj[0]],tempo.conj[0]))
regras_mamdani.append(Regra([sujeira.conj[0],manchas.conj[1]],tempo.conj[2]))
regras_mamdani.append(Regra([sujeira.conj[0],manchas.conj[2]],tempo.conj[3]))
regras_mamdani.append(Regra([sujeira.conj[1],manchas.conj[0]],tempo.conj[1]))
regras_mamdani.append(Regra([sujeira.conj[1],manchas.conj[1]],tempo.conj[2]))
regras_mamdani.append(Regra([sujeira.conj[1],manchas.conj[2]],tempo.conj[3]))
regras_mamdani.append(Regra([sujeira.conj[2],manchas.conj[0]],tempo.conj[2]))
regras_mamdani.append(Regra([sujeira.conj[2],manchas.conj[1]],tempo.conj[3]))
regras_mamdani.append(Regra([sujeira.conj[2],manchas.conj[2]],tempo.conj[4]))

regras_sugeno=[]
regras_sugeno.append(Regra([sujeira.conj[0],manchas.conj[0]],0.5))
regras_sugeno.append(Regra([sujeira.conj[0],manchas.conj[1]],23))
regras_sugeno.append(Regra([sujeira.conj[0],manchas.conj[2]],42))
regras_sugeno.append(Regra([sujeira.conj[1],manchas.conj[0]],10))
regras_sugeno.append(Regra([sujeira.conj[1],manchas.conj[1]],26))
regras_sugeno.append(Regra([sujeira.conj[1],manchas.conj[2]],42))
regras_sugeno.append(Regra([sujeira.conj[2],manchas.conj[0]],27))
regras_sugeno.append(Regra([sujeira.conj[2],manchas.conj[1]],41))
regras_sugeno.append(Regra([sujeira.conj[2],manchas.conj[2]],60))
                 

if __name__ == "__main__":
    entradas=[i*10 for i in range(11)]
    entradas=[entradas,entradas]
    print("Máquina de Lavar Fuzzy")
    while True:
        opcao=0
        print("\n1. Mamdani")
        print("2. Sugeno")
        print("3. Sair")

        while True:
            try:
                opcao = int(input("Escolha uma opção: "))
            except ValueError:
                print("Sua escolha deve ser um número entre 1 e 3")
            if((opcao <= 0) or (opcao > 3)):
                print("Sua escolha deve ser um número entre 1 e 3")
            else:
                break
        if opcao==3:
            sys.exit(0)
        #Mamdani
        elif opcao==1:
            rule_bank_plot(regras_mamdani,0)
            for entrada in itertools.product(*entradas):
                inferencias=[]
                for regra in regras_mamdani:
                    inferencias.append(co.inferencia_mamdani(regra.antecedentes,regra.consequente,entrada,20))

                agregacao=co.uniao(inferencias[0],inferencias[1],20)
                for inferencia in inferencias[2:]:
                    agregacao=co.uniao(agregacao,inferencia,20)
                saida=co.defuzzificacao(agregacao,"",20)
                print(entrada,saida)

        #Sugeno
        else:
            for entrada in itertools.product(*entradas):
                ativacoes=[]
                for regra in regras_sugeno:
                    ativacoes.append(co.inferencia_sugeno(regra.antecedentes,entrada,20))

                numerador=0
                denominador=0
                for i in range(len(regras_sugeno)):
                    numerador+=ativacoes[i]*regras_sugeno[i].consequente
                    denominador+=ativacoes[i]
                saida=numerador/denominador
                print(entrada,saida)
#Final do Loop

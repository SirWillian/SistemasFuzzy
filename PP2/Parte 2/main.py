#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conjunto import Conjunto
from Variavel import Variavel
import ConjuntoOperator as co
import RelacaoOperator as ro

from mpl_toolkits import mplot3d
from matplotlib import cm
import numpy as np
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

altura = Variavel([Conjunto([[1,1],[1.5,0],[2,0]],"baixo"),Conjunto([[1,0],[1.5,1],[2,0]],"medio"),Conjunto([[1,0],[1.5,0],[2,1]],"alto")])
peso = Variavel([Conjunto([[0,1],[50,0],[100,0]],"leve"),Conjunto([[0,0],[50,1],[100,0]],"moderado"),Conjunto([[0,0],[50,0],[100,1]],"pesado")])
forca = Variavel([Conjunto([[0,1],[50,0],[100,0]],"media"),Conjunto([[0,0],[50,1],[100,1]],"forte")])

if __name__ == "__main__":
    while True:
        opcao = 0
        conj_a = altura.conj[2]
        conj_b = peso.conj[2]
        print("\n1. Visualização de premissas")
        print("2. Inferência")
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

        elif opcao==1:
            print("1. Baixo e leve")
            print("2. Altura média e peso moderado")
            print("3. Alto e pesado")
            while True:
                try:
                    opcao = int(input("Escolha uma premissa: "))
                except ValueError:
                    print("Sua escolha deve ser um número entre 1 e 3")
                if((opcao <= 0) or (opcao > 3)):
                    print("Sua escolha deve ser um número entre 1 e 3")
                else:
                    break

            conj_a=altura.conj[opcao-1]
            conj_b=peso.conj[opcao-1]

            n_steps=0
            while True:
                try:
                    n_steps = int(input("Defina o grau de discretização (número de passos): "))
                    break;
                except ValueError:
                    print("Sua escolha deve ser um número inteiro maior que 1")
                if(n_steps<=1):
                    print("Sua escolha deve ser um número inteiro maior que 1")
                else:
                    break
            premissa=co.conjuncao(conj_a,conj_b,n_steps,0)
            surface_plot(premissa)

        else:
            n_steps=0
            while True:
                try:
                    n_steps = int(input("Defina o grau de discretização (número de passos): "))
                    break;
                except ValueError:
                    print("Sua escolha deve ser um número inteiro maior que 1")
                if(n_steps<=1):
                    print("Sua escolha deve ser um número inteiro maior que 1")
                else:
                    break
            
            entrada = co.conjuncao(co.levemente(altura.conj[2], n_steps),co.muito(peso.conj[2],n_steps),n_steps,0)

            regra1 = ro.regra(co.conjuncao(altura.conj[2],peso.conj[2],n_steps,0),forca.conj[1],n_steps)
            regra2 = ro.regra(co.conjuncao(altura.conj[1],peso.conj[1],n_steps,0),co.levemente(forca.conj[1],n_steps),n_steps)
            regra3 = ro.regra(co.conjuncao(altura.conj[0],peso.conj[0],n_steps,0),forca.conj[1],n_steps)

            ext_entrada=ro.expansao_cilindrica(entrada, (0,100), n_steps)

            print("\n1. União das inferências de cada regra")
            print("2. Inferência da união de todas as regras")

            while True:
                try:
                    opcao = int(input("Escolha uma opcção: "))
                except ValueError:
                    print("Sua escolha deve ser 1 ou 2")
                if((opcao <= 0) or (opcao > 2)):
                    print("Sua escolha deve ser 1 ou 2")
                else:
                    break

            conc=0
            if opcao==1:
                infer1=ro.intersecao(regra1,ext_entrada)
                infer2=ro.intersecao(regra2,ext_entrada)
                infer3=ro.intersecao(regra3,ext_entrada)

                conc1=ro.projecao(infer1,2)
                conc2=ro.projecao(infer2,2)
                conc3=ro.projecao(infer3,2)

                conc=co.uniao(conc1,conc2,n_steps)
                conc=co.uniao(conc,conc3,n_steps)
            else:
                regra=ro.uniao(regra1,regra2)
                regra=ro.uniao(regra,regra3)
                infer=ro.intersecao(regra,ext_entrada)
                conc=ro.projecao(infer,2)

            conj_plot(conc)
            
            #Plot aqui maybe
#Final do Loop

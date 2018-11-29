#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conjunto import Conjunto
from Variavel import Variavel
import ConjuntoOperator as co

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

def alpha_cut_plot(regra, n_cuts):
    fig=plt.figure()
    ax=plt.axes(projection="3d")
    
    x=np.unique(np.array(regra)[:,0])
    y=np.unique(np.array(regra)[:,1])
    X,Y = np.meshgrid(x,y)
    zs=np.array(regra)[:,2]
    cuts=np.linspace(0,np.amax(zs),num=n_cuts,endpoint=True)
    for i in reversed(range(len(cuts)-1)):
        z_index=np.logical_and(zs>cuts[i],zs<cuts[i+1])
        zs[z_index]=cuts[i]
        
    Z=zs.reshape(X.shape)
    surf=ax.plot_surface(X,Y,Z,rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0)
    fig.colorbar(surf,shrink=0.5,aspect=5)

    plt.show()
    
    

altura = Variavel([Conjunto([[1,1],[1.5,0]],"baixo"),Conjunto([[1,0],[1.5,1],[2,0]],"medio"),Conjunto([[1.5,0],[2,1]],"alto")])
peso = Variavel([Conjunto([[0,1],[50,0]],"leve"),Conjunto([[0,0],[50,1],[100,0]],"moderado"),Conjunto([[50,0],[100,1]],"pesado")])

if __name__ == "__main__":
    while True:
        opcao = 0
        conj_a = altura.conj[2]
        conj_b = peso.conj[2]
        print("\n1. Se é baixo então é leve")
        print("2. Se tem altura média então tem peso moderado")
        print("3. Se é alto então é pesado")
        print("4. Sair")
        while True:
            try:
                opcao = int(input("Escolha uma regra: "))
            except ValueError:
                print("Sua escolha deve ser um número entre 1 e 4")
            if((opcao <= 0) or (opcao > 4)):
                print("Sua escolha deve ser um número entre 1 e 4")
            else:
                break
        if opcao==4:
            sys.exit(0)

        conj_a=altura.conj[opcao-1]
        conj_b=peso.conj[opcao-1]

        print("\n1. Conjunção (Regra de Mamdani)")
        print("2. Conjunção (Regra de Lassen)")
        print("3. Disjunção")
        print("4. Implicação S")
        print("5. Implicação (Lucasiewicz)")
        print("6. Implicação (Godel)")
        print("7. Implicação (Kleene)")
        print("8. Implicação (Zadeh)")
        
        while True:
            try:
                opcao = int(input("Escolha uma operação: "))
            except ValueError:
                print("Sua escolha deve ser um número entre 1 e 8")
            if((opcao <= 0) or (opcao > 8)):
                print("Sua escolha deve ser um número entre 1 e 8")
            else:
                break

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
        output=[]
        if(opcao==1):
            output=co.conjuncao(conj_a,conj_b,n_steps,0)
        elif(opcao==2):
            output=co.conjuncao(conj_a,conj_b,n_steps,1)
        elif(opcao==3):
            output=co.disjuncao(conj_a,conj_b,n_steps)
        elif(opcao==4):
            output=co.implicacao(conj_a,conj_b,n_steps,"s")
        elif(opcao==5):
            output=co.implicacao(conj_a,conj_b,n_steps,"luca")
        elif(opcao==6):
            output=co.implicacao(conj_a,conj_b,n_steps,"godel")
        elif(opcao==7):
            output=co.implicacao(conj_a,conj_b,n_steps,"kleene")
        elif(opcao==8):
            output=co.implicacao(conj_a,conj_b,n_steps,"zadeh")


        print("1. Plot simples")
        print("2. Plot por alfa-cortes")
        while True:
            try:
                opcao = int(input("Escolha uma regra: "))
            except ValueError:
                print("Sua escolha deve ser 1 ou 2")
            if((opcao <= 0) or (opcao > 2)):
                print("Sua escolha deve ser 1 ou 2")
            else:
                break
        if(opcao==1):
            surface_plot(output)
        else:
            n_cuts=0
            while True:
                try:
                    n_cuts = int(input("Defina o número de alfa-cortes a serem usados: "))
                except ValueError:
                    print("Sua escolha deve ser um número inteiro maior que 1")
                if(n_cuts<=1):
                    print("Sua escolha deve ser um número inteiro maior que 1")
                else:
                    break
            alpha_cut_plot(output,n_cuts)
#Final do Loop

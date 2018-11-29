#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conjunto import Conjunto
from Variavel import Variavel
import ConjuntoOperator as co
import sys

#Inicio do Loop

def nemMuitoAltoEBaixo(alto, baixo):
    conj=co.intersecao(co.negacao(co.muito(alto, True)),co.negacao(baixo))
    for i in range(len(conj.pontos)):
        print(conj.pontos[i])

def pesadoOuNaoMuitoLeve(pesado,leve):
    conj=co.uniao(pesado, co.negacao(co.muito(leve, False)))
    for i in range(len(conj.pontos)):
        print(conj.pontos[i])

def escolherGrupos():
    print("Escolha qual um universo (altura - 1 ou peso - 2) e dois conjuntos (entre 1 e 3).")

    opcao1=0
    opcao2=0
    opcao3=0
    while True:
        try:
            opcao1 = int(input("Escolha o universo: "))
        except:
            pass
        if((opcao1 <= 0) or (opcao1 > 2)):
            print("Escolha 1 ou 2")
        else:
            break
    while True:
        try:
            opcao2 = int(input("Escolha o primeiro conjunto: "))
        except:
            pass
        if((opcao2 <= 0) or (opcao2 > 3)):
            print("Escolha 1, 2 ou 3")
        else:
            break
    while True:
        try:
            opcao3 = int(input("Escolha o segundo conjunto: "))
        except:
            pass
        if((opcao3 <= 0) or (opcao3 > 3)):
            print("Escolha 1, 2 ou 3")
        else:
            break
    return (opcao1,opcao2,opcao3)

altura = Variavel([Conjunto([[1,1],[1.5,0]],"baixo"),Conjunto([[1,0],[1.5,1],[2,0]],"medio"),Conjunto([[1.5,0],[2,1]],"alto")])
peso = Variavel([Conjunto([[0,1],[50,0]],"leve"),Conjunto([[0,0],[50,1],[100,0]],"moderado"),Conjunto([[50,0],[100,1]],"pesado")])

if __name__ == "__main__":
    while True:
        opcao = 0
        print("\n1. União de dois conjuntos de sua escolha")
        print("2. Interseção de dois conjuntos de sua escolha")
        print("3. Visualização do conjunto 'Não muito alto nem baixo'")
        print("4. Visualização do conjunto 'Pesado ou não muito leve'")
        print("5. Sair")
        while True:
            try:
                opcao = int(input("Escolha uma opção: "))
            except ValueError:
                print("Sua escolha deve ser um número entre 1 e 5")
            if((opcao < 0) or (opcao > 5)):
                print("Sua escolha deve ser um número entre 1 e 5")
            else:
                break
        if opcao==1:
            #escolher os grupos
            escolhas=escolherGrupos()
            conj=0
            if(escolhas[0]==1):
                conj=co.uniao(altura.conj[escolhas[1]-1], altura.conj[escolhas[2]-1])
            else:
                conj=co.uniao(peso.conj[escolhas[1]-1], peso.conj[escolhas[2]-1])
            for i in range(len(conj.pontos)):
                print(conj.pontos[i])
                    
        elif opcao==2:
            #escolher os grupos
            escolhas=escolherGrupos()
            conj=0
            if(escolhas[0]==1):
                conj=co.intersecao(altura.conj[escolhas[1]-1], altura.conj[escolhas[2]-1])
            else:
                conj=co.intersecao(peso.conj[escolhas[1]-1], peso.conj[escolhas[2]-1])
            for i in range(len(conj.pontos)):
                print(conj.pontos[i])
            
        elif opcao==3:
            #chamar o metodo
            nemMuitoAltoEBaixo(altura.conj[2],altura.conj[0])
        elif opcao==5:
            sys.exit(0)
        else:
            #chamar o metodo
            pesadoOuNaoMuitoLeve(peso.conj[2],peso.conj[0])


#Final do Loop

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from Subconjuntos import Subconjuntos

#Em python2 troque tkinter para Tkinter

TITLE_FONT = ("Helvetica", 18, "bold")
TEXT_FONT = ("Helvetica", 12)

#cria os subconjuntos definidos na especificação
subconjunto_1b = Subconjuntos([1,1,1,1.5])
subconjunto_1m = Subconjuntos([1,1.5,1.5,2])
subconjunto_1a = Subconjuntos([1.5,2,2,2])

subconjunto_2b = Subconjuntos([1,1,1,1.5])
subconjunto_2m = Subconjuntos([1,1.5,1.5,2])
subconjunto_2a = Subconjuntos([1.65,2,2,2])

subconjunto_3b = Subconjuntos([0.7,1,1,1.5])
subconjunto_3m = Subconjuntos([1,1.4,1.6,2])
subconjunto_3a = Subconjuntos([1.5,1.8,2,2])

conjunto1 = [subconjunto_1b, subconjunto_1m, subconjunto_1a]
conjunto2 = [subconjunto_2b, subconjunto_2m, subconjunto_2a]
conjunto3 = [subconjunto_3b, subconjunto_3m, subconjunto_3a]

conjuntos = [conjunto1, conjunto2, conjunto3]

conjunto_atual=0
subconjunto_atual = 0


def desenha_plot(figure, conj):
    figure.clear()
    a = figure.add_subplot(111)
    cores=["blue","orange","green"]
    for i in range(len(conj)):
        if conj[i].selecionado:
            a.fill(conj[i].pontos,[0,1,1,0], color=cores[i])
        else:
            a.plot(conj[i].pontos,[0,1,1,0], color=cores[i])
    figure.canvas.draw()

def set_conj(frame, number):
    global conjunto_atual
    conjunto_atual = number
    set_subconj(frame, subconjunto_atual, conjunto_atual)

def set_subconj(frame, number, conj):
    subconjunto_atual = number
    for i in range(len(conjuntos[conj])):
        if i == number:
            conjuntos[conj][i].selecionado=True
        else:
            conjuntos[conj][i].selecionado=False
    desenha_plot(frame, conjuntos[conj])

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Sistemas Fuzzy - PP1 Parte 1", font=TITLE_FONT)
        label.place(anchor=tk.N, x=250, y=20)

        labelConj = tk.Label(self, text="Escolha o conjunto de funções de pertinência", font=TEXT_FONT)
        labelConj.place(anchor=tk.W, x=20, y=70)
        
        labelSubconj = tk.Label(self, text="Escolha o subconjunto", font=TEXT_FONT)
        labelSubconj.place(anchor=tk.W, x=20, y=130)

        labelPert = tk.Label(self, text="Pertinência do ponto", font=TEXT_FONT)
        labelPert.place(anchor=tk.W, x=20, y=190)
        t=tk.StringVar()
        entryPert = tk.Entry(self, textvariable=t)
        entryPert.place(anchor=tk.W, x=20, y=210)
        buttonPert = tk.Button(self, text="Check")
        buttonPert.place(anchor=tk.W, x=150, y=210)
        s=tk.StringVar()
        labelPertValor = tk.Label(self, textvariable=s)

        f = Figure(figsize=(5,5), dpi=100)        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(y=300)
        
        buttonB = tk.Button(self, text="Baixo", command=lambda: set_subconj(f, 0,conjunto_atual))
        buttonM = tk.Button(self, text="Médio", command=lambda: set_subconj(f, 1,conjunto_atual))
        buttonA = tk.Button(self, text="Alto", command=lambda: set_subconj(f, 2,conjunto_atual))

        button1 = tk.Button(self, text="Conjunto 1", command=lambda: set_conj(f, 0))
        button2 = tk.Button(self, text="Conjunto 2", command=lambda: set_conj(f, 1))
        button3 = tk.Button(self, text="Conjunto 3", command=lambda: set_conj(f, 2))

        button1.place(x=20,y=85)
        button2.place(x=110,y=85)
        button3.place(x=200,y=85)

        buttonB.place(x=20,y=145)
        buttonM.place(x=80,y=145)
        buttonA.place(x=145,y=145)

        desenha_plot(f, conjuntos[conjunto_atual])

        


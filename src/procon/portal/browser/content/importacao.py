# -*- coding: utf-8 -*-

from Products.Five import BrowserView
import pyexcel as pe
import os


class Importacao(BrowserView):
    """ importar excel de perguntas e respostas """
    URL = "/perguntas_e_respostas_procon_04_05.xlsx"

    def __call__(self):
        dados = {}
        path = os.getcwd()
        rows = pe.get_records(file_name=path + "/excel" + self.URL)
        i = 0
        for row in rows:
            dados[i] = {'Categoria': row['Categoria'],
                        'Pergunta': row['Pergunta'],
                        'Resposta': row['Resposta']}
            i = i + 1
        print dados

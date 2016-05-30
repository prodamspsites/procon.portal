# -*- coding: utf-8 -*-

import pyexcel as pe
import os
from Products.Five import BrowserView
from plone import api
from random import randint
from plone.app.textfield.value import RichTextValue
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


class Importacao(BrowserView):
    """ importar excel de perguntas e respostas """
    FILE = "/perguntas_e_respostas_procon_04_05.xlsx"
    CONTADOR = 0

    def __call__(self):
        path = os.getcwd()
        rows = pe.get_records(file_name=path + "/excel" + self.FILE)
        for row in rows:
            self.criarObjetosPorCategorias(**row)
            self.CONTADOR = self.CONTADOR + 1

    def criarObjetosPorCategorias(self, **kwargs):
        """ criar objetos de Coleção e Perguntas
            dentro de duvidas.
        @returns: Booleano criação de objetos plone
        """
        # print kwargs['Pergunta']
        portal = api.portal.get()
        folder = portal['duvidas']
        folder = folder['categorias']
        categoria_normalize = kwargs['Categoria']
        if categoria_normalize:
            cleanID = getUtility(IIDNormalizer)
            categoria_normalize = cleanID.normalize(categoria_normalize)
            # print categoria_normalize

            if categoria_normalize not in folder.objectIds():
                folder.invokeFactory('Folder', categoria_normalize)
            categoria = folder[categoria_normalize]
            pergunta_id = 'pergunta' + str(randint(0, 99999))

            if kwargs['Pergunta'] and kwargs['Resposta']:
                categoria.invokeFactory('pergunta',
                                        pergunta_id,
                                        pergunta=RichTextValue(kwargs['Pergunta'], 'text/html', 'text/x-html-safe', encoding='utf-8'),
                                        resposta=RichTextValue(kwargs['Resposta'], 'text/html', 'text/x-html-safe', encoding='utf-8'))
                categoria.reindexObject(pergunta_id)

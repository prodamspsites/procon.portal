# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api


class Reclamacao(BrowserView):

    def buscaReclamacao(self):
        portal = api.portal.get()
        folderConsumidor = portal['denuncia']
        form = folderConsumidor['formulario-de-denuncia']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()

        dados = [x for x in dados if type(x) is list]

        # import pdb; pdb.set_trace()

        return dados

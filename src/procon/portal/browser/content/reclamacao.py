# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api


class Reclamacao(BrowserView):

    def buscaReclamacao(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formID']
        sendDataAdapter = form['adapterID']
        dados = sendDataAdapter.getSavedFormInputItems()

        dados = [x for x in dados if type(x) is list]

        # import pdb; pdb.set_trace()

        return dados

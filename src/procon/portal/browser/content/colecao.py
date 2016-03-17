# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api
from DateTime import DateTime


class Noticias(BrowserView):
    def getDate(self, date):
        data = DateTime(date).strftime('%d/%m/%Y')
        hora = DateTime(date).strftime('%H:%M')
        return data + ' às ' + hora


class Colecao(BrowserView):
    def getFilteredContent(self):
        portal = api.portal.get()
        secao = self.context.secaoID
        path = '/'.join(portal.getPhysicalPath()) + '/' + secao

        try:
            filtro = self.request.form['SearchableText']
        except:
            filtro = None

        searchPergunta = self.context.portal_catalog(path=path, portal_type="pergunta", SearchableText=filtro)
        searchResposta = self.context.portal_catalog(path=path, portal_type="resposta", SearchableText=filtro)

        items = searchPergunta + searchResposta

        items = [x.getObject() for x in items]

        if searchPergunta and searchResposta:
            lista1 = [x.getObject() for x in searchPergunta]
            lista2 = [x.getObject() for x in searchResposta if x.getObject().aq_parent not in lista1]

            items = lista1 + lista2

        return items

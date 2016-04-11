# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api
from DateTime import DateTime


class Noticias(BrowserView):
    def getDate(self, date):
        data = DateTime(date).strftime('%d/%m/%Y')
        hora = DateTime(date).strftime('%H:%M')
        return data + ' - ' + hora


class Colecao(BrowserView):
    def getFilteredContent(self):
        portal = api.portal.get()
        secao = self.context.secaoID
        path = '/'.join(portal.getPhysicalPath()) + '/' + secao

        try:
            filtro = self.request.form['SearchableText']
        except:
            filtro = None

        items = self.context.portal_catalog(path=path,
                                            portal_type="pergunta",
                                            SearchableText=filtro)

        return items

    def getUser(self):
        user = api.user.get_current()
        user.getProperty('name')
        return user

# -*- coding: utf-8 -*-
import json
from plone.app.layout.viewlets import ViewletBase
from plone import api
from plone.dexterity.utils import createContentInContainer
from pymongo import MongoClient
from procon.portal import MONGODB_HOSTS


class Duvidas(ViewletBase):
    diretorio = "Categorias"

    def criaDiretorio(self):
        """ cria diretorios para consumidor """
        portal = api.portal.get()
        if self.diretorio not in portal.objectIds():
            self.montaEstrutura()
        else:
            del portal[self.diretorio]
            self.montaEstrutura()

    def consultaDiretorio(self):
        """ consulta diretorios para consumidor """
        self.request.response.setHeader("Content-type", "application/json")
        return self.consulta()

    def montaEstrutura(self):
            portal = api.portal.get()
            portal.invokeFactory('Folder', self.diretorio)
            consumidor = portal[self.diretorio]
            print "criado diretorio" + self.diretorio
            consumidor.reindexObject()
            folder = portal[self.diretorio]
            categorias = self.categorias()
            for categoria in categorias:
                nome = categoria['name']
                url = categoria['url']
                categoria = categoria['category']
                print 'criado objeto de url' + url
                createContentInContainer(folder,
                                         'Link',
                                         title=nome,
                                         remoteUrl=url,
                                         categoria=categoria
                                         )

    def categorias(self):
        """ categorias do site consumidor.gov.br """
        client = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
        db = client.consumidor
        categorias = db.empresas.find()
        return categorias

    def consulta(self):
        portal = api.portal.get()
        catalog = portal.portal_catalog
        links = catalog(portal_type="Link")
        dados = []
        cont = 0
        if links:
            for i in links:
                result = i.getObject()
                dados.append({'titulo': result.title,
                              'categoria': result.categoria,
                              'url': result.remoteUrl
                              })
                cont = cont + 1
            dados_to_json = json.dumps(dados, ensure_ascii=False)
            return dados_to_json

# -*- coding: utf-8 -*-
import json
from Products.Five import BrowserView
from plone import api
from plone.dexterity.utils import createContentInContainer
from pymongo import MongoClient


class Consumidor(BrowserView):
    diretorio = "categoria"

    def criaDiretorio(self):
        """ cria diretorios para consumidor """
        portal = api.portal.get()
        if self.diretorio not in portal.objectIds():
            self.montaEstrutura(portal)
        else:
            del portal[self.diretorio]
            self.montaEstrutura(portal)

    def consultaDiretorio(self):
        """ consulta diretorios para consumidor """
        self.request.response.setHeader("Content-type", "application/json")
        return self.consulta()

    def montaEstrutura(self, portal):
        portal.invokeFactory('Folder', self.diretorio)
        diretorio = portal[self.diretorio]
        diretorio.reindexObject()
        categorias = self.categorias()
        folder = portal[self.diretorio]
        for categoria in categorias:
            nome = categoria['name']
            url = categoria['url']
            categoria = categoria['category']
            print 'criado objeto de url' + url
            objeto = createContentInContainer(folder,
                                              'Link',
                                              title=nome,
                                              remoteUrl=url,
                                              categoria=categoria
                                              )
            portal.portal_workflow.doActionFor(objeto, 'publish')

    def categorias(self):
        """ categorias do site consumidor.gov.br """
        try:
            # client = MongoClient("prodam.mongodb", 80)
            client = MongoClient("mongodb.hom.prodam", 27017)
            db = client.consumidor
            categorias = db.empresas.find()
        except Exception, ex:
            print ex
        print categorias
        return categorias

    def consulta(self):
        portal = api.portal.get()
        folder = portal[self.diretorio]
        catalog = folder.portal_catalog
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

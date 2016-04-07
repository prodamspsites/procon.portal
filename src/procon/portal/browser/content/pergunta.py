# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from pymongo import MongoClient
from datetime import datetime


class BuscarDuvidas(BrowserView):

    def buscarPerguntaResposta(self):
        """ buscar registros mongodb do tire suas dúvidas """
        try:
            client = MongoClient()
            db = client.consumidor
            perguntas = db.tbl_replica.find()
            return perguntas
        except Exception, ex:
            print ex


class SalvarDuvidas(BrowserView):

    def salvarPerguntaResposta(self, id_plone,
                               util,
                               pergunta,
                               usuario,
                               resposta,
                               assunto,
                               mensagem):

        """ salvar registros mongodb do tire suas duvidas """
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            client = MongoClient()
            db = client.consumidor
            db.tbl_replica.insert({"id_plone": id_plone,
                                   "util": util,
                                   "pergunta": pergunta,
                                   "resposta": resposta,
                                   "data": data,
                                   "assunto": assunto,
                                   "mensagem": mensagem,
                                   "usuario": usuario})
        except Exception, ex:
            print ex

    def __call__(self):
        radio_util = self.getRadio()
        pergunta = self.getPergunta()
        resposta = self.getResposta()
        assunto = self.getAssunto()
        mensagem = self.getMensagem()
        usuario = self.getUsuario()

        self.salvarPerguntaResposta("id-all", radio_util,
                                    pergunta,
                                    usuario,
                                    resposta,
                                    assunto,
                                    mensagem)

    def getRadio(self):
        try:
            req = self.request.form['util']
        except:
            req = None
        return req

    def getPergunta(self):
        try:
            req = self.request.form['pergunta']
        except:
            req = None
        return req

    def getResposta(self):
        try:
            req = self.request.form['resposta']
        except:
            req = None
        return req

    def getAssunto(self):
        try:
            req = self.request.form['assunto']
        except:
            req = None
        return req

    def getMensagem(self):
        try:
            req = self.request.form['mensagem']
        except:
            req = None
        return req

    def getUsuario(self):
        try:
            req = self.request.form['usuario']
        except:
            req = None
        return req

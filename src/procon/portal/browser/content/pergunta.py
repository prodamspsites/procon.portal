# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from pymongo import MongoClient
from datetime import datetime


class Pergunta(BrowserView):

    def buscarPerguntaRespostaMongoDb(self):
        """ buscar registros mongodb do tire suas dúvidas """
        try:
            client = MongoClient()
            db = client.consumidor
            perguntas = db.perguntas.find()
            return perguntas
        except Exception, ex:
            print ex

    def salvarPerguntaRespostaMongoDb(self, id_plone, util, pergunta, usuario, resposta, assunto, mensagem):
        """ salvar registros mongodb do tire suas duvidas """
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            client = MongoClient()
            db = client.consumidor
            db.replica.insert({"id_plone": id_plone,
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

        print radio_util
        print pergunta
        print resposta

        if radio_util and pergunta and resposta:
            self.buscarPerguntaRespostaMongoDb()
        else:
            self.salvarPerguntaRespostaMongoDb("id-3", 1, "perg", "pato", "resp", "assu", "msg")

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

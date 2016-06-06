# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from plone import api


class BuscarDuvidas(BrowserView):

    def buscarPerguntaResposta(self):
        """ buscar registros mongodb do tire suas dúvidas """
        try:
            client = MongoClient()
            db = client.consumidor
            perguntas = {}
            if self.getFiltro():
                questionarios = db.tbl_replica.find({"usuario": {"$regex": self.getFiltro()}})
                perguntas = {'perguntas': questionarios, 'filtro': self.getFiltro(), 'total': questionarios.count()}
                return perguntas
            else:
                questionarios = db.tbl_replica.find()
                if questionarios.count() < 1:
                    return False
                else:
                    perguntas = {'perguntas': questionarios, 'filtro': None, 'total': questionarios.count()}
                    return perguntas

        except Exception:
            return False

    def getFiltro(self):
        try:
            req = self.request.form['filtro_nome']
        except:
            req = None
        return req


class SalvarDuvidas(BrowserView):

    def salvarPerguntaResposta(self, id_plone,
                               util,
                               pergunta,
                               usuario,
                               resposta,
                               assunto,
                               categoria,
                               mensagem):
        user = api.user.get_current()
        userID = user.id
        """ salvar registros mongodb do tire suas duvidas """
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            client = MongoClient()
            db = client.consumidor

            if self.getIdentificacao() and not self.getObservacao():

                identificacao = self.getIdentificacao()
                db.tbl_replica.update_one({"_id": ObjectId(identificacao)},
                                          {"$set": {"lido": True, "operador": userID}},
                                          upsert=False)
            elif self.getIdentificacao() and self.getObservacao():
                identificacao = self.getIdentificacao()
                observacao = self.getObservacao()
                db.tbl_replica.update_one({"_id": ObjectId(identificacao)},
                                          {"$set": {"observacao": observacao, "operador": userID}},
                                          upsert=False)
            else:
                db.tbl_replica.insert({"id_plone": id_plone,
                                       "util": util,
                                       "lido": False,
                                       "pergunta": pergunta,
                                       "resposta": resposta,
                                       "data": data,
                                       "assunto": assunto,
                                       "mensagem": mensagem,
                                       "categoria": categoria,
                                       "observacao": "",
                                       "operador": False,
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
        categoria = self.getCategoria()

        self.salvarPerguntaResposta("id-all",
                                    radio_util,
                                    pergunta,
                                    usuario,
                                    resposta,
                                    assunto,
                                    categoria,
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

    def getIdentificacao(self):
        try:
            req = self.request.form['identificacao']
        except:
            req = None
        return req

    def getObservacao(self):
        try:
            req = self.request.form['observacao']
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

    def getCategoria(self):
        try:
            req = self.request.form['categoria']
        except:
            req = None
        return req

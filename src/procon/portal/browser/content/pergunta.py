# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from plone import api
from procon.portal import MONGODB_HOSTS


class BuscarDuvidas(BrowserView):

    def buscarPerguntaResposta(self):
        """ buscar registros mongodb do tire suas dúvidas """
        try:
            client = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
            db = client.consumidor
            perguntas = {}
            filtro = self.getFiltro()
            dropdown = self.getDropDown()
            if filtro and dropdown:
                if dropdown == "lido" and filtro == "sim":
                    filtro_real = 'sim'
                    questionarios = db.tbl_replica.find({dropdown: True})
                    perguntas = {'perguntas': questionarios, 'status': dropdown, 'filtro': filtro_real, 'total': questionarios.count()}
                elif dropdown == "lido" and filtro != "sim":
                    filtro_real = 'não'
                    questionarios = db.tbl_replica.find({dropdown: False})
                    perguntas = {'perguntas': questionarios, 'status': dropdown, 'filtro': filtro_real, 'total': questionarios.count()}
                else:
                    questionarios = db.tbl_replica.find({dropdown: {"$regex": filtro}})
                    perguntas = {'perguntas': questionarios, 'status': dropdown, 'filtro': filtro, 'total': questionarios.count()}

                return perguntas
            else:
                questionarios = db.tbl_replica.find()
                if questionarios.count() < 1:
                    perguntas = {'perguntas': None, 'filtro': None, 'status': None, 'total': None}
                    return perguntas
                else:
                    perguntas = {'perguntas': questionarios, 'filtro': None, 'status': None, 'total': questionarios.count()}
                    return perguntas

        except Exception:
            return False

    def getDropDown(self):
        try:
            req = self.request.form['dropdown_ftr']
        except:
            req = None
        return req

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
            client = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
            db = client.consumidor
            print self.request.form
            if self.getIdentificacao() and not self.getObservacao() and not self.getStatus():
                print ' n ok'
                identificacao = self.getIdentificacao()

                db.tbl_replica.update_one({"_id": ObjectId(identificacao)},
                                          {"$set": {"lido": True, "operador": userID, "data_atualizacao": data}},
                                          upsert=False)
            elif self.getIdentificacao() and self.getObservacao() and not self.getStatus():
                print 'n ok'
                identificacao = self.getIdentificacao()
                observacao = self.getObservacao()
                db.tbl_replica.update_one({"_id": ObjectId(identificacao)},
                                          {"$set": {"observacao": observacao, "operador": userID, "data_atualizacao": data}},
                                          upsert=False)
            elif self.getIdentificacao() and self.getStatus():
                print 'ok'
                identificacao = self.getIdentificacao()
                status = self.getStatus()
                db.tbl_replica.update_one({"_id": ObjectId(identificacao)},
                                          {"$set": {"status": status, "operador": userID, "data_atualizacao": data}},
                                          upsert=False)
            else:
                print 'nao ok'
                db.tbl_replica.insert_one({"id_plone": id_plone,
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
                                           "status": "Não Processada",
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

    def getStatus(self):
        try:
            req = self.request.form['status']
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

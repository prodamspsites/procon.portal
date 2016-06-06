# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api
from pymongo import MongoClient
from datetime import datetime


class SelecionarReclamacao(BrowserView):

    def __call__(self):
        user = api.user.get_current()
        userID = user.id
        mongodb = MongoClient()
        db = mongodb.procon
        protocolo = self.getProtocolo()
        questionarios = db.tbl_replica.find({"protocolo": {"$regex": protocolo}})
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if questionarios.count() > 0:

            db.tbl_replica.update_one({"protocolo": protocolo},
                                      {"$set": {"lido": False}},
                                      upsert=False)
        else:
            db.reclamacoes.insert_one({"status": "Selecione uma opção",
                                       "protocolo": protocolo,
                                       "lido": True,
                                       "operador": userID,
                                       "data": data})

    def getProtocolo(self):
        try:
            return self.request.form['protocolo']
        except Exception:
            return None


class AtualizarReclamacao(BrowserView):

    def __call__(self):
        return self.AtualizarReclamacao()

    def getStatus(self):
        try:
            return self.request.form['reclamacao_status']
        except Exception:
            return None

    def getProtocolo(self):
        try:
            return self.request.form['protocolo']
        except Exception:
            return None

    def AtualizarReclamacao(self):
        user = api.user.get_current()
        userID = user.id
        mongodb = MongoClient()
        db = mongodb.procon
        find = db.reclamacoes.find({"protocolo": {"$regex": self.getProtocolo()}})
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if find.count() == 0:
            db.reclamacoes.insert_one({"status": self.getStatus(),
                                       "protocolo": self.getProtocolo(),
                                       "lido": False,
                                       "operador": userID,
                                       "data": data})
        else:
            db.reclamacoes.update_one({"protocolo": self.getProtocolo()},
                                      {"$set": {"status": self.getStatus(), "data": data}},
                                      upsert=False)


class Reclamacao(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

        mongodb = MongoClient()
        self.db = mongodb.procon

    def buscaReclamacao(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formularios']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()

        dados = [x for x in dados if type(x) is list]

        for dado in dados:
            protocolo = dado[-1]
            query = self.db.reclamacoes.find_one({"protocolo": {"$regex": str(protocolo)}})
            try:
                dado.insert(len(dado), query['status'].encode('utf-8'))
            except TypeError:
                continue
            try:
                dado.insert(len(dado) + 1, query['lido'])
            except KeyError:
                continue
        return dados

    def buscaDenuncia(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formulario-de-denuncia']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()

        dados = [x for x in dados if type(x) is list]

        return dados

    def buscaFornecedor(self):
        portal = api.portal.get()
        folderConsumidor = portal['fornecedor']
        form = folderConsumidor['adesao-ao-procon-paulistano']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()

        dados = [x for x in dados if type(x) is list]

        return dados

    def reclamacaoStatus(self):
        return ['Selecione uma opção',
                'Em processamento',
                'Concluído – Extra-Procon',
                'Concluído – Simples consulta',
                'Aguarda resposta do fornecedor',
                'Aguarda retorno do consumidor',
                'Baixa de CIP - improcedência',
                'Baixa de CIP – com resolução total',
                'Baixa de CIP – com resolução parcial',
                'Baixa de CIP – resolução por mera liberalidade',
                'Baixa de CIP – sem resolução',
                'Baixa de CIP – desistência do consumidor',
                'Baixa de CIP – decurso (fornecedor)',
                'Instauração de reclamação',
                'Notificação para defesa e/ou audiência enviada',
                'Aguarda prazo de defesa/audiência',
                'Em análise',
                'Decisão – reclamação não fundamentada',
                'Decisão – reclamação fundamentada atendida',
                'Decisão – reclamação fundamentada não atendida']

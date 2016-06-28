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
        questionarios = db.reclamacoes.find({"protocolo": {"$regex": protocolo}})
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if questionarios.count() > 0:

            db.reclamacoes.update_one({"protocolo": protocolo},
                                      {"$set": {"lido": True, "operador": userID}},
                                      upsert=False)
        else:
            db.reclamacoes.insert_one({"status": "Selecione uma opção",
                                       "protocolo": protocolo,
                                       "lido": True,
                                       "FA": False,
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
            return False

    def getFA(self):
        try:
            return self.request.form['FA']
        except Exception:
            return False

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
        coluna = self.getStatus() and 'status' or self.getFA() and 'FA'
        valor = self.getStatus() or self.getFA()
        if find.count() == 0:
            db.reclamacoes.insert_one({"status": self.getStatus(),
                                       "protocolo": self.getProtocolo(),
                                       "lido": False,
                                       "FA": self.getFA(),
                                       "operador": userID,
                                       "data": data})
        else:
            db.reclamacoes.update_one({"protocolo": self.getProtocolo()},
                                      {"$set": {coluna: valor, "data": data, "operador": userID}},
                                      upsert=False)


class AtualizaForms(BrowserView):

    def __call__(self):
        if self.getTable() and self.getObjectId() and self.getColumn() and self.getValue():
            self.atualizaFormularios()

    def getColumn(self):
        try:
            return self.request.form['campo']
        except Exception:
            return None

    def getValue(self):
        try:
            return self.request.form['valor']
        except Exception:
            return None

    def getTable(self):
        try:
            return self.request.form['area']
        except Exception:
            return None

    def getObjectId(self):
        try:
            return self.request.form['objId']
        except Exception:
            return None

    def atualizaFormularios(self):
        mongodb = MongoClient()
        db = mongodb.procon

        table = self.getTable()
        objId = self.getObjectId()
        column = self.getColumn()
        value = self.getValue()
        user = api.user.get_current()
        userID = user.id
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        lido = column == 'lido' and value or False
        observacao = column == 'observacao' and value or False
        FA = column == 'FA' and value or False

        find_one = db[table].find_one({'data': {"$regex": objId}})
        if not find_one:
            db[table].insert_one({'data': objId,
                                  'observacao': observacao,
                                  "lido": lido,
                                  "FA": FA,
                                  "operador": userID,
                                  "data_atualizacao": data})
        else:
            db[table].update_one({'data': objId}, {"$set": {column: value, "operador": userID, "data_atualizacao": data}}, upsert=False)


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
        dados = [x for x in dados if type(x) is list and self.filterInputs(x)]

        for dado in dados:
            print len(dado)
            if (len(dado) == 53 and dado[42] != 'NO UPLOAD') or (len(dado) == 50 and dado[42] == 'NO UPLOAD'):
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
            protocolo = dado[-6]
            query = self.db.reclamacoes.find_one({"protocolo": {"$regex": str(protocolo)}})
            try:
                dado[-5] = query['FA']
                dado[-4] = query['status'].encode('utf-8')
                dado[-3] = query['lido']
                dado[-2] = query['operador']
                dado[-1] = query['data']
            except:
                pass
        return dados

    def filtraForm(self):
        try:
            filtro = self.request.form['filtro']
            filtro = filtro.lower().split(' ')
            return filtro
        except:
            return False

    def buscaDenuncia(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formulario-de-denuncia']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()
        dados = [x for x in dados if type(x) is list and self.filterInputs(x)]

        for dado in dados:
	    print len(dado)
	    print dado
            if (len(dado) == 21 and dado[15] != 'NO UPLOAD') or (len(dado)==18 and dado[15] == 'NO UPLOAD'):
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
            query = self.db.denuncias.find_one({"data": {"$regex": str(dado[-6])}})
            try:
                dado[-4] = query['lido']
                dado[-3] = query['observacao']
                dado[-2] = query['operador']
                dado[-1] = query['data_atualizacao']
            except:
                pass

        return dados

    def filterInputs(self, lista):
        filtro = self.filtraForm()
        if filtro:
            verifica = False
            for items in lista:
                item = str(items).lower().split(' ')
                if any(i in filtro for i in item):
                    verifica = True
            return verifica
        else:
            return True

    def buscaFornecedor(self):
        portal = api.portal.get()
        folderConsumidor = portal['fornecedor']
        form = folderConsumidor['adesao-ao-procon-paulistano']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()
        dados = [x for x in dados if type(x) is list and self.filterInputs(x)]

        for dado in dados:
            print dado
            if (len(dado) == 25 and dado[21] != 'NO UPLOAD') or (len(dado)==22 and dado[21] == 'NO UPLOAD'):
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
            query = self.db.fornecedores.find_one({"data": {"$regex": str(dado[-6])}})

            try:
                dado[-4] = query['lido']
                dado[-3] = query['observacao']
                dado[-2] = query['operador']
                dado[-1] = query['data_atualizacao']
            except:
                pass

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

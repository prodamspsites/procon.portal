# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api
from pymongo import MongoClient
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from procon.portal import MONGODB_HOSTS


class SelecionarReclamacao(BrowserView):

    def __call__(self):
        user = api.user.get_current()
        userID = user.id
        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
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
        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
        db = mongodb.procon
        find = db.reclamacoes.find({"protocolo": {"$regex": self.getProtocolo()}})
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        coluna = self.getStatus() and 'status' or self.getFA() and 'FA'
        status = self.getStatus() or 'Selecione uma opção'
        valor = self.getStatus() or self.getFA()
        if find.count() == 0:
            db.reclamacoes.insert_one({"status": status,
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
        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
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
        tratativas = column == 'tratativas' and value or False
        FA = column == 'FA' and value or False

        find_one = db[table].find_one({'data': {"$regex": objId}})
        if not find_one:
            db[table].insert_one({'data': objId,
                                  'observacao': observacao,
                                  "lido": lido,
                                  "FA": FA,
                                  "tratativas": tratativas,
                                  "operador": userID,
                                  "data_atualizacao": data})
        else:
            db[table].update_one({'data': objId}, {"$set": {column: value, "operador": userID, "data_atualizacao": data}}, upsert=False)


class Reclamacao(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
        self.db = mongodb.procon

    def buscaReclamacao(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formularios']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()
        dados = [x for x in dados if type(x) is list and self.filterInputs(x)]

        for dado in dados:
            if len(dado) == 58:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
                dado.insert(len(dado) + 5, '')
                dado.insert(len(dado) + 6, '')
                dado.insert(len(dado) + 7, '')
                dado.insert(len(dado) + 8, '')
            protocolo = dado[-10]
            query = self.db.reclamacoes.find_one({"protocolo": {"$regex": str(protocolo)}})
            try:
                mt = getToolByName(self.context, 'portal_membership')
                user = mt.getMemberById(dado[0])
                idade = user.getProperty('adicional_um')
                deficiencia = user.getProperty('campo_adicional_tres')
                doenca = user.getProperty('campo_doenca_grave')
                dado[-9] = dado[-4] and 'Sim' or 'Não'
                dado[-8] = user.getProperty('razao_social') or user.getProperty('fullname') or user
                dado[-7] = user.getProperty('razao_social') and 'Pessoa jurídica' or 'Pessoa física'
                dado[-6] = (idade == deficiencia and deficiencia == doenca and 'Não') or 'Sim'
                dado[-5] = query['FA']
                dado[-4] = query['status']
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

    def filtraColuna(self):
        try:
            coluna = self.request.form['coluna']
            coluna = coluna
            return coluna
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
            if len(dado) == 24:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
                dado.insert(len(dado) + 5, '')
                dado.insert(len(dado) + 6, '')
                dado.insert(len(dado) + 7, '')
                dado.insert(len(dado) + 8, '')
            query = self.db.denuncias.find_one({"data": {"$regex": str(dado[-11])}})
            try:
                mt = getToolByName(self.context, 'portal_membership')
                user = mt.getMemberById(dado[0])
                idade = user.getProperty('adicional_um')
                deficiencia = user.getProperty('campo_adicional_tres')
                doenca = user.getProperty('campo_doenca_grave')
                dado[-9] = dado[-4] and 'Sim' or 'Não'
                dado[-8] = user.getProperty('razao_social') or user.getProperty('fullname') or user
                dado[-7] = user.getProperty('razao_social') and 'Pessoa jurídica' or 'Pessoa física'
                dado[-6] = (idade == deficiencia and deficiencia == doenca and 'Não') or 'Sim'
                dado[-5] = user
                dado[-4] = query['lido']
                dado[-3] = query['observacao']
                dado[-2] = query['operador']
                dado[-1] = query['data_atualizacao']
            except:
                pass

        return dados

    def filterInputs(self, lista):
        if self.filtraColuna():
            novaLista = []
            novaLista.append(lista[int(self.filtraColuna())])
        filtro = self.filtraForm()
        if filtro:
            verifica = False
            lista = novaLista or lista
            for items in lista:
                item = str(items).lower().split(' ')
                if any(i in filtro for i in item):
                    verifica = True
                elif filtro in item:
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
            if len(dado) == 29:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
            query = self.db.fornecedores.find_one({"data": {"$regex": str(dado[-7])}})

            try:
                dado[-5] = query['tratativas']
                dado[-4] = query['lido']
                dado[-3] = query['observacao']
                dado[-2] = query['operador']
                dado[-1] = query['data_atualizacao']
            except:
                pass

        return dados

    def reclamacaoStatus(self):
        return ['Não processada',
                'Aguarda prospecção do fornecedor',
                'Em processamento',
                'Em prospecção do fornecedor',
                'Concluído – Extra-Procon',
                'Concluído – Simples consulta',
                'Encerrado por domicílio inconsistente',
                'Encerrado – desistência do consumidor',
                'Aguarda resposta do fornecedor',
                'Aguarda retorno do consumidor',
                'Baixa de CIP - improcedência',
                'Baixa de CIP – Litispendência',
                'Baixa de CIP – com resolução total',
                'Baixa de CIP – com resolução parcial',
                'Baixa de CIP – resolução por mera liberalidade',
                'Baixa de CIP – sem resolução',
                'Baixa de CIP – desistência do consumidor',
                'Baixa de CIP – decurso (fornecedor)',
                'Enviado para a Fiscalização/TACs e Ações Judiciais',
                'Adesão do Fornecedor Concluída',
                'Instauração de reclamação',
                'Notificação para defesa e/ou audiência enviada',
                'Aguarda prazo de defesa/audiência',
                'Em análise',
                'Decisão – litispendência',
                'Decisão – reclamação não fundamentada',
                'Decisão – reclamação fundamentada atendida',
                'Decisão – reclamação fundamentada não atendida']

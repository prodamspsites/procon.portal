# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api
from pymongo import MongoClient
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from procon.portal import MONGODB_HOSTS
import logging
from plone.memoize import ram
from time import time
from math import ceil
from itertools import izip as zip, count
from dateutil.parser import parse
from datetime import datetime

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num



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
        find = db.reclamacoes.find({"dataId": {"$regex": self.getProtocolo()}})
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        coluna = self.getStatus() and 'status' or self.getFA() and 'FA'
        status = self.getStatus() or 'Selecione uma opção'
        valor = self.getStatus() or self.getFA()
        db.backofficeLog.insert_one({"operador": userID,
                                     "data": data,
                                     "backoffice": "reclamação",
                                     "alteracao_campo": coluna,
                                     "alteracao_valor": valor,
                                     "protocolo": self.getProtocolo()})
        if self.getFA:
            db.FAlog.insert_one({"operador": userID,
                                 "data": data,
                                 "protocolo": self.getProtocolo()})
        if find.count() == 0:
            db.reclamacoes.insert_one({"status": status,
                                       "dataId": self.getProtocolo(),
                                       "lido": False,
                                       "cProtocolo": '',
                                       "show": 'yes',
                                       "FA": self.getFA(),
                                       "operador": userID,
                                       "data": data})
        else:
            db.reclamacoes.update_one({"dataId": self.getProtocolo()},
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
        cProtocolo = column == 'cProtocolo' and value or False
        FA = column == 'FA' and value or False

        find_one = db[table].find({'data': {"$regex": objId}})
        db.backofficeLog.insert_one({"operador": userID,
                                     "data": data,
                                     "backoffice": table,
                                     "alteracao_campo": column,
                                     "alteracao_valor": value,
                                     "protocolo": objId})
        if not find_one:
            db[table].insert_one({'data': objId,
                                  'dataId': objId,
                                  'observacao': observacao,
                                  "lido": lido,
                                  "FA": FA,
                                  "cProtocolo": cProtocolo,
                                  "tratativas": tratativas,
                                  "operador": userID,
                                  "data_atualizacao": data})
        else:
            if table == 'reclamacoes':
            	db[table].update({'dataId': {"$regex": str(objId)}}, { "$set": { str(column): str(value), "operador": str(userID), "data_atualizacao": str(data)}}, multi=True, upsert=False)
            else:
                db[table].update({'data': {"$regex": str(objId)}}, { "$set": { str(column): str(value), "operador": str(userID), "data_atualizacao": str(data)}}, multi=True, upsert=False)


class Reclamacao(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
        self.db = mongodb.procon
        self.dados = self.getReclamacoes()
        self.pg = self.getPg() or 1
        self.limit = 20
        self.pagination = Pagination(self.pg, self.limit, len(self.dados))

    def getReclamacoes(self):
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
            if len(dado) == 59:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
                dado.insert(len(dado) + 5, '')
                dado.insert(len(dado) + 6, '')
                dado.insert(len(dado) + 7, '')
                if dado[-11] == 'x':
                    dado[-11] = dado[-10]
                if len(dado[-10]) == 19:
                    dado[-10] = dado[-9]
        dados = sorted(dados, key=lambda x: datetime.strptime(x[-11], '%d/%m/%Y %H:%M:%S'), reverse=True)
        dados = [[i,d] for i, d in zip(count(), dados)]
        return dados
 

    def getPg(self):
        try:
            pg = self.request.form['pg']
            print 'pg: %s' % pg
        except:
            pg = 1
            print 'except'
        return int(pg)


    def getDetailNumber(self):
        try:
            return self.request.form['detailNumber']
        except Exception:
            return None

    def buscaReclamacaoDetalhes(self):
        numero = self.getDetailNumber()
        dados = self.buscaReclamacaoCompleta() 

        return dados[int(numero)]

    def showDenuncias(self, dado):
        data = dado[-11]
        query = self.db.denuncias.find_one({"data": {"$regex": str(data)}})
        try:
            show = query['show']
            return show and True or False
        except:
            return True


    def show(self, dado):
        data = dado[-11]
        query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(data)}})
        try:
            show = query['show']
            return show and True or False
        except:
            return True 

    def getLog(self, protocolo):
        query = self.db.backofficeLog.find({"protocolo": {"$regex": str(protocolo)}})
        return query


    def getCProtocolo(self, dado):
        protocolo = dado[-10]
        data = dado[-11]
        query = self.db.reclamacoes.find_one({"dataId": {"$regex": data}})
        try:
            protocolo = query['cProtocolo'] or protocolo
        except:
            pass
        return protocolo


    def buscaReclamacao(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit

        for dado in dados[b_start:b_end]:
            _dado = dado[1]
            if len(_dado) == 58:
                dado[1].insert(len(_dado), '')
                dado[1].insert(len(_dado) + 1, '')
                dado[1].insert(len(_dado) + 2, '')
                dado[1].insert(len(_dado) + 3, '')
                dado[1].insert(len(_dado) + 4, '')
                dado[1].insert(len(_dado) + 5, '')
                dado[1].insert(len(_dado) + 6, '')
                dado[1].insert(len(_dado) + 7, '')
                dado[1].insert(len(_dado) + 8, '')
            if len(_dado) == 59:
                dado[1].insert(len(_dado), '')
                dado[1].insert(len(_dado) + 1, '')
                dado[1].insert(len(_dado) + 2, '')
                dado[1].insert(len(_dado) + 3, '')
                dado[1].insert(len(_dado) + 4, '')
                dado[1].insert(len(_dado) + 5, '')
                dado[1].insert(len(_dado) + 6, '')
                dado[1].insert(len(_dado) + 7, '')
            protocolo = _dado[-11]
            query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(protocolo)}})

            try:
                mt = getToolByName(self.context, 'portal_membership')
                user = mt.getMemberById(_dado[0])
                idade = user.getProperty('adicional_um')
                deficiencia = user.getProperty('campo_adicional_tres')
                doenca = user.getProperty('campo_doenca_grave')
                dado[1][-9] = _dado[-4] and 'Sim' or 'Não'
                dado[1][-8] = user.getProperty('razao_social') or user.getProperty('fullname') or user
                dado[1][-7] = user.getProperty('razao_social') and 'Pessoa jurídica' or 'Pessoa física'
                dado[1][-6] = (idade == deficiencia and deficiencia == doenca and 'Não') or 'Sim'
                dado[1][-5] = query['FA']
                dado[1][-4] = query['status']
                dado[1][-3] = query['lido']
                dado[1][-2] = query['operador']
                dado[1][-1] = query['data']
            except Exception,e:
                print str(e)
        return dados[b_start:b_end]

    def buscaReclamacaoCompleta(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit

        for dado in dados:
            _dado = dado[1]
            if len(_dado) == 58:
                dado[1].insert(len(_dado), '')
                dado[1].insert(len(_dado) + 1, '')
                dado[1].insert(len(_dado) + 2, '')
                dado[1].insert(len(_dado) + 3, '')
                dado[1].insert(len(_dado) + 4, '')
                dado[1].insert(len(_dado) + 5, '')
                dado[1].insert(len(_dado) + 6, '')
                dado[1].insert(len(_dado) + 7, '')
                dado[1].insert(len(_dado) + 8, '')
            if len(_dado) == 59:
                dado[1].insert(len(_dado), '')
                dado[1].insert(len(_dado) + 1, '')
                dado[1].insert(len(_dado) + 2, '')
                dado[1].insert(len(_dado) + 3, '')
                dado[1].insert(len(_dado) + 4, '')
                dado[1].insert(len(_dado) + 5, '')
                dado[1].insert(len(_dado) + 6, '')
                dado[1].insert(len(_dado) + 7, '')
            protocolo = _dado[-11]
            query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(protocolo)}})

            try:
                mt = getToolByName(self.context, 'portal_membership')
                user = mt.getMemberById(dado[0])
                idade = user.getProperty('adicional_um')
                deficiencia = user.getProperty('campo_adicional_tres')
                doenca = user.getProperty('campo_doenca_grave')
                dado[1][-9] = _dado[-4] and 'Sim' or 'Não'
                dado[1][-8] = user.getProperty('razao_social') or user.getProperty('fullname') or user
                dado[1][-7] = user.getProperty('razao_social') and 'Pessoa jurídica' or 'Pessoa física'
                dado[1][-6] = (idade == deficiencia and deficiencia == doenca and 'Não') or 'Sim'
                dado[1][-5] = query['FA']
                dado[1][-4] = query['status']
                dado[1][-3] = query['lido']
                dado[1][-2] = query['operador']
                dado[1][-1] = query['data']
            except:
                pass
        return dados




    def filtraForm(self):
        try:
            filtro = self.request.form['filtro']
            filtro = filtro.lower()
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

    def buscaDenunciaDetalhe(self):
        numero = self.getDetailNumber()
        dados = self.buscaDenuncia() 
        return dados[int(numero)]

    def buscaDenuncia(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formulario-de-denuncia']
        sendDataAdapter = form['dados']
        dados = sendDataAdapter.getSavedFormInput()
        dados = [x for x in dados if type(x) is list and self.filterInputs(x)]

        for dado in dados[b_start:b_end]:
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

        return dados[b_start:b_end]

    def filterInputs(self, lista):
        novaLista = []
        if self.filtraColuna():
            novaLista = []
            novaLista.append(lista[int(self.filtraColuna())])
        filtro = self.filtraForm()
        if filtro:
            verifica = False
            lista = novaLista or lista
            for items in lista:
                item = str(items).lower()
                if filtro in item:
                    verifica = True
                return verifica
        else:
            return True

    def buscaFornecedorDetalhe(self):
        numero = self.getDetailNumber()
        dados = self.buscaFornecedor()
        return dados[int(numero)]

    def buscaFornecedor(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit


        for dado in dados[b_start:b_end]:
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

        return dados[b_start:b_end]

    def getPaginacao(self):
        return self.pagination

    def reclamacaoStatus(self):
        return ['Não processada',
                'Aguarda prospecção do fornecedor',
                'Em processamento',
                'Em prospecção do fornecedor',
                'Concluído - Atendimento Preliminar',
                'Concluído – Extra-Procon',
                'Concluído – Simples consulta',
                'Encerrado por domicílio inconsistente',
                'Encerrado – desistência do consumidor',
                'Encerrado – Duplicidade',
                'Encerrado – Litispendência',
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


class Fornecedor(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
        self.db = mongodb.procon
        portal = api.portal.get()
        folderConsumidor = portal['fornecedor']
        form = folderConsumidor['adesao-ao-procon-paulistano']
        sendDataAdapter = form['dados']
        self.dados = sendDataAdapter.getSavedFormInput()
        self.dados = [x for x in self.dados if type(x) is list and self.filterInputs(x)]
        self.pg = self.getPg() or 1
        self.limit = 20
        self.pagination = Pagination(self.pg, self.limit, len(self.dados))


    def getPg(self):
        try:
            pg = self.request.form['pg']
        except:
            pg = 1
        return int(pg)


    def getDetailNumber(self):
        try:
            return self.request.form['detailNumber']
        except Exception:
            return None

    def buscaReclamacaoDetalhes(self):
        numero = self.getDetailNumber()
        dados = self.dados 

        return dados[int(numero)]

    def showDenuncias(self, dado):
        data = dado[-11]
        query = self.db.denuncias.find_one({"data": {"$regex": str(data)}})
        try:
            show = query['show']
            return show and True or False
        except:
            return True


    def show(self, dado):
        data = dado[-11]
        query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(data)}})
        try:
            show = query['show']
            return show and True or False
        except:
            return True 

    def getCProtocolo(self, dado):
        protocolo = dado[-10]
        data = dado[-11]
        query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(data)}})
        try:
            protocolo = query['cProtocolo'] or protocolo
        except:
            pass
        return protocolo


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
            protocolo = dado[-11]
            query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(protocolo)}})

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
            filtro = filtro.lower()
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

    def buscaDenunciaDetalhe(self):
        numero = self.getDetailNumber()
        dados = self.buscaDenuncia() 
        return dados[int(numero)]

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
        novaLista = []
        if self.filtraColuna():
            novaLista = []
            novaLista.append(lista[int(self.filtraColuna())])
        filtro = self.filtraForm()
        if filtro:
            verifica = False
            lista = novaLista or lista
            for items in lista:
                item = str(items).lower().split(' ')
                for i in item:
                    if filtro in i:
                        verifica = True
                return verifica
        else:
            return True

    def buscaFornecedorDetalhe(self):
        numero = self.getDetailNumber()
        dados = self.buscaFornecedorCompleta()
        return dados[int(numero)]

    def buscaFornecedor(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit

        for dado in dados[b_start:b_end]:
            if len(dado) == 29:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
            if len(dado) == 30:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado[-5] = dado[-6]
                dado[-7] = dado[-6]

            query = self.db.fornecedores.find_one({"data": {"$regex": str(dado[-7])}})


            try:
                dado[-5] = query['tratativas']
                dado[-4] = query['lido']
                dado[-3] = query['observacao']
                dado[-2] = query['operador']
                dado[-1] = query['data_atualizacao']
            except:
                pass

        return dados[b_start:b_end]

    def buscaFornecedorCompleta(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit


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




    def getPaginacao(self):
        return self.pagination

    def reclamacaoStatus(self):
        return ['Não processada',
                'Aguarda prospecção do fornecedor',
                'Em processamento',
                'Em prospecção do fornecedor',
                'Concluído - Atendimento Preliminar',
                'Concluído – Extra-Procon',
                'Concluído – Simples consulta',
                'Encerrado por domicílio inconsistente',
                'Encerrado – desistência do consumidor',
                'Encerrado – Duplicidade',
                'Encerrado – Litispendência',
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

class Denuncia(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

        mongodb = MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
        self.db = mongodb.procon
        self.dados = self.getDenuncias()
        self.pg = self.getPg() or 1
        self.limit = 20
        self.pagination = Pagination(self.pg, self.limit, len(self.dados))



    def getDenuncias(self):
        portal = api.portal.get()
        folderConsumidor = portal['consumidor']
        form = folderConsumidor['formulario-de-denuncia']
        sendDataAdapter = form['dados']
        print dir(sendDataAdapter)
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
            if len(dado) == 25:
                dado.insert(len(dado), '')
                dado.insert(len(dado) + 1, '')
                dado.insert(len(dado) + 2, '')
                dado.insert(len(dado) + 3, '')
                dado.insert(len(dado) + 4, '')
                dado.insert(len(dado) + 5, '')
                dado.insert(len(dado) + 6, '')
                dado.insert(len(dado) + 7, '')
                if dado[-11] == 'x':
                    dado[-11] = dado[-10]
        return dados


    def getPg(self):
        try:
            pg = self.request.form['pg']
        except:
            pg = 1
        return int(pg)


    def getDetailNumber(self):
        try:
            return self.request.form['detailNumber']
        except Exception:
            return None

    def buscaReclamacaoDetalhes(self):
        numero = self.getDetailNumber()
        dados = self.dados 

        return dados[int(numero)]

    def showDenuncias(self, dado):
        data = dado[-11]
        query = self.db.denuncias.find_one({"data": {"$regex": str(data)}})
        try:
            show = query['show']
            return show and True or False
        except:
            return True


    def show(self, dado):
        data = dado[-11]
        query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(data)}})
        try:
            show = query['show']
            return show and True or False
        except:
            return True 

    def getCProtocolo(self, dado):
        protocolo = dado[-10]
        data = dado[-11]
        query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(data)}})
        try:
            protocolo = query['cProtocolo'] or protocolo
        except:
            pass
        return protocolo


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
            protocolo = dado[-11]
            query = self.db.reclamacoes.find_one({"dataId": {"$regex": str(protocolo)}})

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
            filtro = filtro.lower()
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

    def buscaDenunciaDetalhe(self):
        numero = self.getDetailNumber()
        dados = self.buscaDenunciaCompleta() 
        return dados[int(numero)]

    def buscaDenuncia(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit

        for dado in dados:
#            print 'lero'
            for i in dado:
                if type(i) is str:
                   if 'ROBSON' in i:
                       print i

        for dado in dados[b_start:b_end]:
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
                mt = getToolByName(self.context, 'portal_membership')
                user = mt.getMemberById(dado[0])
                pass


        return dados[b_start:b_end]

    def buscaDenunciaCompleta(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit

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
        novaLista = []
        if self.filtraColuna():
            novaLista = []
            novaLista.append(lista[int(self.filtraColuna())])
        filtro = self.filtraForm()
        if filtro:
            verifica = False
            lista = novaLista or lista
            for items in lista:
                item = str(items).lower().split(' ')
                for i in item:
                    if filtro in i:
                        verifica = True
                return verifica
        else:
            return True

    def buscaFornecedorDetalhe(self):
        numero = self.getDetailNumber()
        dados = self.buscaFornecedor()
        return dados[int(numero)]

    def buscaFornecedor(self):
        dados = self.dados
        pagination = self.pagination
        limit = self.limit
        b_start = (pagination.page * limit) - limit
        b_end = pagination.page * limit


        for dado in dados[b_start:b_end]:
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

        return dados[b_start:b_end]

    def getPaginacao(self):
        return self.pagination

    def reclamacaoStatus(self):
        return ['Não processada',
                'Aguarda prospecção do fornecedor',
                'Em processamento',
                'Em prospecção do fornecedor',
                'Concluído - Atendimento Preliminar',
                'Concluído – Extra-Procon',
                'Concluído – Simples consulta',
                'Encerrado por domicílio inconsistente',
                'Encerrado – desistência do consumidor',
                'Encerrado – Duplicidade',
                'Encerrado – Litispendência',
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

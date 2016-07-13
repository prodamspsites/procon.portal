# -*- coding: utf-8 -*-
# flake8: noqa
from procon.portal.config import MONGODB_HOSTS
from datetime import datetime
from Products.Five import BrowserView
from lib import *
import pymongo


class ProtocoloView(BrowserView):

    def __init__(self, context, request):
        """
        USAGE
        Create Protocol:
        1 - Call with ajax http://{server-url}/Procon/@@protocolo
        2 - Set 'action' body variable with value 'create' or 'update' on request.
        3 - Get return of request to use anywhere.
            'create' returns protocol number and HTTP Code 200.
        Update Protocol:
        1 - Call with ajax http://{server-url}/Procon/@@protocolo
        2 - Set 'action','protocol' body variables with respective values 'update','{protocol-number}' on request.
        3 - Get return of request to use anywhere.
            'update' returns a success message and HTTP Code 200.
        """
        self.request = request
        self.context = context

    def __call__(self):
        """
        Here the request method is filtered to accept only POST requests and call a CREATE or UPDATE function based on
        action "create" or "update".
        """
        if self.request["REQUEST_METHOD"] == 'POST':
            self.current_year = datetime.now().year

            # Here the MONGODB_HOSTS need to be changed based on site environment!
            self.conn = pymongo.MongoClient(MONGODB_HOSTS["host"], MONGODB_HOSTS["port"])
            self.db = self.conn.procon
            self.collection = self.db.protocolo

            if 'action' in self.request:
                if self.request.get('action') == 'create':
                    return self.create()
                if self.request.get('action') == 'update':
                    if 'protocol' in self.request and self.request.get('protocol'):
                        return self.update(self.request.get('protocol'))

    def create(self):
        """
        This function create a PROTOCOL NUMBER based on current year and sequential number with 'pending' state on
        mongodb and returns the protocol number.
        """
        protocol = self.collection.find().sort('protocolo', pymongo.DESCENDING).limit(1)
        if not protocol.count():
            protocol = 5555
        else:
            protocol = int(protocol[0]['protocolo']) + 1

        self.collection.insert_one({
            'ano': str(self.current_year),
            'protocolo': str(protocol).rjust(8, '0'),
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'state': 'pending'
        })

        self.request.response.setStatus(self, 200)
        return '{}{}'.format(self.current_year, str(protocol).rjust(8, '0'))

    def update(self, protocol):
        """
        This function update a saved PROTOCOL NUMBER to state 'done';
        """
        result = self.collection.update_one(
            {'ano': protocol[:4], 'protocolo': protocol[4:]},
            {
                '$set': {
                    'state': 'done'
                }
            }
        )

        if not result.matched_count:
            self.request.response.setStatus(self, 404)
            return 'ERRO! Protocolo {} não existe!'.format(protocol)

        if result.modified_count:
            self.request.response.setStatus(self, 200)
            return 'SUCESSO! Protocolo {} atualizado!'.format(protocol)

        if result.matched_count and not result.modified_count:
            self.request.response.setStatus(self, 404)
            return 'ATENÇÃO! Protocolo {} já atualizado!'.format(protocol)

# -*- coding: utf-8 -*-
import socket
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('procon.portal')

# configuração ambientes MongoDB
MONGODB_HOSTS = {}
hostname = socket.gethostbyname(socket.gethostname())

MONGODB_HOSTS["host"] = "mongo0.prodam"
MONGODB_HOSTS["port"] = 27017


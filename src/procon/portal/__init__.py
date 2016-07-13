# -*- coding: utf-8 -*-
import socket
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('procon.portal')

# configuração ambientes MongoDB
MONGODB_HOSTS = {}
hostname = socket.gethostbyname(socket.gethostname())

if hostname == "127.0.0.1" or "10.20.26.20":
    MONGODB_HOSTS["host"] = "localhost"
    MONGODB_HOSTS["port"] = "27017"

elif hostname == "10.20.25.200":
    MONGODB_HOSTS["host"] = "mongo0.prodam"
    MONGODB_HOSTS["port"] = "27017"

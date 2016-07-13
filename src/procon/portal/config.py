# -*- coding: utf-8 -*-
import socket

PROJECTNAME = 'procon.portal'

# http://www.tinymce.com/wiki.php/Configuration:formats
TINYMCE_JSON_FORMATS = {'strikethrough': {'inline': 'span',
                                          'classes': 'strikethrough',
                                          'exact': 'true'},
                        'underline': {'inline': 'span',
                                      'classes': 'underline',
                                      'exact': 'true'}}
# configuração ambientes MongoDB
MONGODB_HOSTS = {}
hostname = socket.gethostbyname(socket.gethostname())

if hostname == "127.0.0.1" or "10.20.26.20":
    MONGODB_HOSTS["host"] = "localhost"
    MONGODB_HOSTS["port"] = "27017"

elif hostname == "10.20.25.200":
    MONGODB_HOSTS["host"] = "mongo0.prodam"
    MONGODB_HOSTS["port"] = "27017"

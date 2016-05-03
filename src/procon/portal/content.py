# -*- coding: utf-8 -*-

from nfe.portal.interfaces import IPergunta, IResposta
from plone.dexterity.content import Item
from plone.dexterity.content import Container
from zope.interface import implements
from plone.indexer import indexer
from five import grok


class Pergunta(Container):
    implements(IPergunta)


@indexer(IPergunta)
def searchableText(obj):
    return u' '.join([obj.pergunta.output])

grok.global_adapter(searchableText, name='SearchableText')


class Resposta(Item):
    implements(IResposta)


@indexer(IPergunta)
def searchableText(obj):
    return ' '.join([obj.resposta.output])

grok.global_adapter(searchableText, name='SearchableText')

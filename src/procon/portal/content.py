# -*- coding: utf-8 -*-

from procon.portal.interfaces import IPergunta
from plone.dexterity.content import Container
from zope.interface import implements
from plone.indexer import indexer
from five import grok


class Pergunta(Container):
    implements(IPergunta)


@indexer(IPergunta)
def searchableText(obj):
    text = u' '.join([obj.pergunta.output])
    text += u' '.join([obj.resposta.output])

    return text

grok.global_adapter(searchableText, name='SearchableText')

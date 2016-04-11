# -*- coding: utf-8 -*-

from procon.portal.interfaces import IPergunta
from plone.indexer.decorator import indexer


@indexer(IPergunta)
def PerguntaSearchableIndex(obj):
    text = u' '.join([obj.pergunta.output])
    text += u' '.join([obj.resposta.output])
    return text

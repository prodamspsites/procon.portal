# -*- coding: utf-8 -*-

from nfe.portal.interfaces import IPergunta
from nfe.portal.interfaces import IResposta
from plone.indexer.decorator import indexer


@indexer(IPergunta)
def PerguntaSearchableIndex(obj):
    return u' '.join([obj.pergunta.output])


@indexer(IResposta)
def RespostaSearchableIndex(obj):
    return u' '.join([obj.resposta.output])

# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements


class iServicos(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(u'Title of the rendered portlet'),
        required=True)

    show_header = schema.Bool(
        title=_(u'Show portlet header'),
        description=_(u''),
        required=True,
        default=False)

    duvidas = schema.Bool(
        title=_(u'Ativar link de dúvidas'),
        description=_(u''),
        required=True,
        default=False)

    duvidas_url = schema.TextLine(
        title=_(u'URL do link de dúvidas'),
        description=_(u''),
        required=False)

    reclamacoes = schema.Bool(
        title=_(u'Ativar link de reclamações'),
        description=_(u''),
        required=True,
        default=False)

    reclamacoes_url = schema.TextLine(
        title=_(u'URL do link de reclamações'),
        description=_(u''),
        required=False)

    hide = schema.Bool(
        title=_(u'Hide portlet'),
        description=_(u'Tick this box if you want to temporarily hide '
                      'the portlet without losing your information.'),
        required=True,
        default=False)


class Assignment(base.Assignment):

    implements(iServicos)

    def __init__(self, header=u'', show_header=False, duvidas=None, duvidas_url=None, reclamacoes=None, reclamacoes_url=None, hide=False):
        self.header = header
        self.show_header = show_header
        self.duvidas = duvidas
        self.duvidas_url = duvidas_url
        self.reclamacoes = reclamacoes
        self.reclamacoes_url = reclamacoes_url
        self.hide = hide

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return 'Twitter'


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/servicos.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return not self.data.hide

    def getTitle(self):
        if self.data.header:
            return self.data.header
        else:
            return 'Twitter'

    def getDuvidas(self):
        if self.data.duvidas:
            return self.data.duvidas
        else:
            return False

    def getDuvidasUrl(self):
        if self.data.duvidas_url:
            return self.data.duvidas_url
        else:
            return False

    def getReclamacoes(self):
        if self.data.reclamacoes:
            return self.data.reclamacoes
        else:
            return False

    def getReclamacoesUrl(self):
        if self.data.reclamacoes_url:
            return self.data.reclamacoes_url
        else:
            return False


class AddForm(base.AddForm):
    form_fields = form.Fields(iServicos)
    label = _(u'Add Service Portlet')
    description = _(u'Show last events')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(iServicos)
    label = _(u'Edit Service Portlet')
    description = _(u'Show last events')

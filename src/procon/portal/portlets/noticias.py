# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements
from plone import api


class iNoticias(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(u'Title of the rendered portlet'),
        required=True)

    show_header = schema.Bool(
        title=_(u'Show portlet header'),
        description=_(u''),
        required=True,
        default=False)

    count = schema.TextLine(
        title=_(u'Quantidade de itens'),
        description=_(u''),
        required=False)

    showFooter = schema.Bool(
        title=_(u'Ativar rodapé'),
        description=_(u''),
        required=True,
        default=False)

    footerText = schema.TextLine(
        title=_(u'Texto do rodapé'),
        description=_(u''),
        required=False)

    footerUrl = schema.TextLine(
        title=_(u'URL do rodapé'),
        description=_(u''),
        required=False)

    hide = schema.Bool(
        title=_(u'Hide portlet'),
        description=_(u'Tick this box if you want to temporarily hide '
                      'the portlet without losing your information.'),
        required=True,
        default=False)


class Assignment(base.Assignment):

    implements(iNoticias)

    def __init__(self, header=u'', show_header=False, count=None, showFooter=None, footerText=None, footerUrl=None, hide=False):
        self.header = header
        self.show_header = show_header
        self.count = count
        self.showFooter = showFooter
        self.footerText = footerText
        self.footerUrl = footerUrl
        self.hide = hide

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return 'Últimas notícias'


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/noticias.pt')

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

    def getNewsItems(self):
        if self.data.count:
            count = int(self.data.count)
        else:
            count = 5
        portal = api.portal.get()
        news = portal.portal_catalog(portal_type="News Item", review_state="published", sort_on="Date", sort_order="reverse")[:count]

        return news

    def getCount(self):
        if self.data.count:
            return self.data.count
        else:
            return False

    def showFooter(self):
        if self.data.showFooter:
            return self.data.showFooter
        else:
            return False

    def getFooterText(self):
        if self.data.footerText:
            return self.data.footerText
        else:
            return 'Ver todas as notícias'

    def getFooterUrl(self):
        if self.data.footerUrl:
            return self.data.footerUrl
        else:
            return False


class AddForm(base.AddForm):
    form_fields = form.Fields(iNoticias)
    label = _(u'Add News Portlet')
    description = _(u'Show news items')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(iNoticias)
    label = _(u'Edit News Portlet')
    description = _(u'Show news items')

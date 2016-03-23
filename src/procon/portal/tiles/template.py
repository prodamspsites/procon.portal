# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from procon.portal import _
from zope import schema
from zope.interface import implements


class IPageTemplate(IPersistentCoverTile):

    template = schema.TextLine(
        title=_(u'Page template'),
        required=True,
    )


class PageTemplate(PersistentCoverTile):

    implements(IPageTemplate)

    index = ViewPageTemplateFile('templates/template.pt')

    is_configurable = True
    is_editable = True
    is_droppable = False
    short_name = _(u'Page template', default=u'Page Template')

    def is_empty(self):
        return not (self.data.get('template', None))

    def accepted_ct(self):
        """Return an empty list as no content types are accepted."""
        return []

    def getTemplate(self):
        nome = str(self.data.get('template', None))
        try:
            template = self.context.restrictedTraverse(nome)
            return template.render()
        except:
            pass

        return False

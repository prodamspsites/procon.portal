# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api


class Navegacao(ViewletBase):
    def isActive(self, obj):
        pass
        context = self.context
        if obj == context:
            return True
        else:
            return False

    def segundoNivel(self, obj):
        try:
            if obj.exibir_menu_de_segundo_nivel:
                if not obj.hasProperty('segundoNivel'):
                    obj.manage_addProperty(id='segundoNivel', type='boolean', value=True)
                if not obj.hasProperty('currentPath'):
                    path = '/'.join(obj.getPhysicalPath())
                    obj.manage_addProperty(id='currentPath', type='string', value=path)
                if not obj.hasProperty('segundonivel_titulo'):
                    titulo = obj.Title()
                    obj.manage_addProperty(id='segundonivel_titulo', type='string', value=titulo)
                else:
                    return True
            else:
                if obj.hasProperty('currentPath'):
                    return True
                else:
                    return False

        except AttributeError:
            if obj.hasProperty('currentPath'):
                return True
            else:
                return False

    def getMenu(self):
        portal = api.portal.get()
        objs = portal.listFolderContents(contentFilter={"portal_type": ["Folder", "Link"]})

        return objs

    def getSegundoNivel(self, obj):
        try:
            folder = obj.restrictedTraverse(obj.currentPath)
            return folder.getFolderContents()
        except:
            return False

    def checkVisibility(self, obj):
        try:
            if obj.hasProperty('segundoNivel'):
                return False
            else:
                return True
        except AttributeError:
            return True

    def getMember(self):
        return api.user.get_current()

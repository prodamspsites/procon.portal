# -*- coding: utf-8 -*-
from Products.Five import BrowserView


class Reclamacao(BrowserView):

    def buscaReclamacao(self):
        cols = self.getColumnNames()

        for row in self.getSavedFormInput():
            print self.rowAsColDict(row, cols)

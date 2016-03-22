# -*- coding: utf-8 -*-
import smtplib
from Products.Five import BrowserView


class DisparaEmail(BrowserView):

    def enviaEmail(self):
        """classe responsavel por gerenciar I/O E-mails"""
        sender = 'teste@teste.com.br'
        receivers = ['vbalvares@prodam.sp.gov.br']
        message = """From: From Person <from@fromdomain.com>
        To: To Person <to@todomain.com>
        MIME-Version: 1.0
        Content-type: text/html
        Subject: SMTP HTML e-mail test

        Teste E-mail

        <b>This is HTML message.</b>
        <h1>This is headline.</h1>
        """
        try:
            smtpObj = smtplib.SMTP('smtpcorp.prodam', 25)
            smtpObj.sendmail(sender, receivers, message)
            print "Successfully sent email"
        except Exception, e:
            print e

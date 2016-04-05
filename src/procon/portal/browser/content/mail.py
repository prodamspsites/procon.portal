# -*- coding: utf-8 -*-
import smtplib
from Products.Five import BrowserView


class DisparaEmail(BrowserView):

    def enviaEmail(self):
        """classe responsavel por gerenciar I/O E-mails"""
        sender = 'pp9810@prefeitura.sp.gov.br'
        receivers = ['pigaov10@gmail.com',
                     'eabueno@gmail.com']
        message = """From: PP9810 <pp9810@prefeitura.sp.gov.br>
                     \nSubject: SMTP HTML e-mail test
                    \n\nTeste E-mail
                  """
        try:
            smtpObj = smtplib.SMTP('smtpcorp.prodam', 25)
            smtpObj.sendmail(sender, receivers, message)
            print "Successfully sent email"
        except Exception, e:
            print e

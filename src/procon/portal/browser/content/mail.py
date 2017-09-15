# -*- coding: utf-8 -*-
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from plone import api
from Products.Five import BrowserView


class Mail(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context
        self.anexos = {}

    def send_mail(self, files=True, send_from = 'noreply@prodam.sp.gov.br', send_to=['shank.sa@gmail.com'], subject='Extrato diário dos backoffices', text='Seguem anexos os extratos exportados dos backoffices.',
                  server="smtpcorp.prodam:25"):
        assert isinstance(send_to, list)


        if files:
            files = ['reclamacoes', 'denuncias', 'fornecedores']
            self.getDadosFromForm(files)

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for a in self.anexos or []:
            part = MIMEApplication(
                self.anexos[a],
                Name=a
            )
            part['Content-Disposition'] = 'attachment; filename="%s.csv"' % a 
            msg.attach(part)


        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()


    def getDadosFromForm(self, files):
        portal = api.portal.get()
        if 'reclamacoes' in files:
            sendDataAdapter = portal['consumidor']['formularios']['dados']
            self.anexos['reclamacoes'] = sendDataAdapter.anexo_csv()
        if 'denuncias' in files:
            sendDataAdapter = portal['consumidor']['formulario-de-denuncia']['dados']
            self.anexos['denuncias'] = sendDataAdapter.anexo_csv()
        if 'fornecedores' in files:
            sendDataAdapter = portal['fornecedor']['adesao-ao-procon-paulistano']['dados']
            self.anexos['fornecedores'] = sendDataAdapter.anexo_csv()



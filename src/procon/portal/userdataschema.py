# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapts
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from z3c.form import field
from z3c.form.browser.radio import RadioFieldWidget

from plone.supermodel import model
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.app.users.browser.register import RegistrationForm, AddUserForm
from plone.z3cform.fieldsets import extensible

from procon.portal.interfaces import IProdamPortal
from procon.portal import _


tipo_options = SimpleVocabulary([
    SimpleTerm(value='pf', title=_(u'Pessoa Física')),
    SimpleTerm(value='pj', title=_(u'Pessoa Jurídica')), ])

municipio_options = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

genero_options = SimpleVocabulary([
    SimpleTerm(value='masculino', title=_(u'Masculino')),
    SimpleTerm(value='feminino', title=_(u'Feminino')), ])

estadocivil_options = SimpleVocabulary([
    SimpleTerm(value='solteiro', title=_(u'Solteiro(a)')),
    SimpleTerm(value='casado', title=_(u'Casado(a)')),
    SimpleTerm(value='separado', title=_(u'Separado(a)')),
    SimpleTerm(value='divorciado', title=_(u'Divorciado(a)')),
    SimpleTerm(value='viuvo', title=_(u'Viúvo(a)')), ])


def validateAccept(value):
    if value is not True:
        return False
    return True


class IEnhancedUserDataSchema(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """
    municipio = schema.Choice(
        title=_(u'1) O consumidor deve assinalar se possui ou não domicílio no Município de São Paulo.', default=u'1) O consumidor deve assinalar se possui ou não domicílio no Município de São Paulo.'),
        description=_(u'Você possui domicílio no Município de São Paulo?',
                      default=u""),
        vocabulary=municipio_options,
        required=True,)
    tipo = schema.Choice(
        title=_(u'', default=u''),
        description=_(u'',
                      default=u""),
        vocabulary=tipo_options,
        required=True,)
    nome = schema.TextLine(
        title=_(u'Nome Completo', default=u'Nome Completo'),
        description=_(u'',
                      default=u""),
        required=False,)
    razao_social = schema.TextLine(
        title=_(u'Razão social', default=u'Razão social'),
        description=_(u'',
                      default=u""),
        required=False,)
    nome_fantasia = schema.TextLine(
        title=_(u'Nome fantasia', default=u'Nome fantasia'),
        description=_(u'',
                      default=u""),
        required=False,)
    responsavel = schema.TextLine(
        title=_(u'Nome completo do responsável', default=u'Nome completo do responsável'),
        description=_(u'',
                      default=u""),
        required=False,)
    cpf = schema.TextLine(
        title=_(u'CPF', default=u'CPF'),
        description=_(u'',
                      default=u""),
        required=False,)
    rg = schema.TextLine(
        title=_(u'RG', default=u'RG'),
        description=_(u'',
                      default=u""),
        required=False,)
    expeditor = schema.TextLine(
        title=_(u'Órgão Expeditor', default=u'Órgão Expeditor'),
        description=_(u'',
                      default=u""),
        required=False,)
    genero = schema.Choice(
        title=_(u'Sexo', default=u'Sexo'),
        description=_(u'',
                      default=u""),
        vocabulary=genero_options,
        required=False,)
    estadocivil = schema.Choice(
        title=_(u'Estado civil', default=u'Estado civil'),
        description=_(u'',
                      default=u""),
        vocabulary=estadocivil_options,
        required=False,)


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, UserDataPanel)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields = fields.omit('accept')  # Users have already accepted.
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        self.add(fields)


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, RegistrationForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        self.add(fields)


class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, AddUserForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields)

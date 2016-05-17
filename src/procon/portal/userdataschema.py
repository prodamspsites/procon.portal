# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapts
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from z3c.form import field
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget

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

adicionais_escolha_um = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

adicionais_escolha_dois = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

adicionais_escolha_tres = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

termos = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Eu concordo com os Termos de Uso do Consumidor.'))])


def validateAccept(value):
    if value is not True:
        return False
    return True


class IEnhancedUserDataSchema(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    termos_uso = schema.List(title=u"Termos de Uso do Consumidor.",
                             # description=u"Eu concordo com os Termos de Uso do Consumidor.",
                             required=True,
                             value_type=schema.Choice(vocabulary=termos)
                             )

    adicional_um = schema.Choice(title=_(u'Possui mais de 60 anos ?'),
                                 description=_(u'Possui mais de 60 anos ?'),
                                 vocabulary=adicionais_escolha_um,
                                 required=True,)

    adicional_um = schema.Choice(title=_(u'Possui mais de 60 anos ?'),
                                 description=_(u'Possui mais de 60 anos ?'),
                                 vocabulary=adicionais_escolha_um,
                                 required=True,)

    adicional_tres = schema.Choice(title=_(u'Possui alguma deficiência ?'),
                                   description=_(u'Possui alguma deficiência ?'),
                                   vocabulary=adicionais_escolha_tres,
                                   required=True,)

    adicional_dois = schema.Choice(title=_(u'Portador de alguma doença grave prevista na Lei nº 12.008/09, atestada por declaração/laudo médico ?'),
                                   description=_(u'Portador de alguma doença grave prevista na Lei nº 12.008/09, atestada por declaração/laudo médico ?'),
                                   vocabulary=adicionais_escolha_dois,
                                   required=True,)

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

    data_nascimento = schema.TextLine(
        title=_(u'Data de nascimento', default=u'Data de nascimento'),
        required=True
    )

    contato_telefone = schema.TextLine(
        title=_(u'DDD + Telefone/Celular'),
        required=True
    )

    contato_celular = schema.TextLine(
        title=_(u'DDD + Telefone/Celular'),
        required=False
    )

    codigo_enderecamento_postal = schema.TextLine(
        title=_(u'CEP', default=u'CEP'),
        required=True
    )

    logradouro = schema.TextLine(
        title=_(u'Logradouro'),
        required=False
    )

    complemento = schema.TextLine(
        title=_(u'Número/Complemento'),
        required=True
    )

    bairro = schema.TextLine(
        title=_(u'Bairro'),
        required=True
    )

    cidade = schema.TextLine(
        title=_(u'Cidade'),
        required=False
    )

    unidade_federativa = schema.TextLine(
        title=_(u'UF'),
        required=False
    )

    site = schema.TextLine(
        title=_(u'Site'),
        required=False
    )

    mail = schema.TextLine(
        title=_(u'E-mail'),
        required=True
    )

    confirmacao = schema.TextLine(
        title=_(u'Confirmação de E-mail'),
        required=True
    )


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
        fields['adicional_um'].widgetFactory = RadioFieldWidget
        fields['adicional_dois'].widgetFactory = RadioFieldWidget
        fields['adicional_tres'].widgetFactory = RadioFieldWidget
        fields['termos_uso'].widgetFactory = CheckBoxFieldWidget
        self.add(fields)


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, RegistrationForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        fields['adicional_um'].widgetFactory = RadioFieldWidget
        fields['adicional_dois'].widgetFactory = RadioFieldWidget
        fields['adicional_tres'].widgetFactory = RadioFieldWidget
        fields['termos_uso'].widgetFactory = CheckBoxFieldWidget

        self.add(fields)


class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, AddUserForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        fields['adicional_um'].widgetFactory = RadioFieldWidget
        fields['adicional_dois'].widgetFactory = RadioFieldWidget
        fields['adicional_tres'].widgetFactory = RadioFieldWidget
        fields['termos_uso'].widgetFactory = CheckBoxFieldWidget

        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields)

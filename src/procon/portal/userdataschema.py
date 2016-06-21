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
    SimpleTerm(value='pessoa física', title=_(u'Pessoa Física')),
    SimpleTerm(value='pessoa jurídica', title=_(u'Pessoa Jurídica')), ])

municipio_options = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

genero_options = SimpleVocabulary([
    SimpleTerm(value='masculino', title=_(u'Masculino')),
    SimpleTerm(value='feminino', title=_(u'Feminino')), ])

estadocivil_options = SimpleVocabulary([
    SimpleTerm(value='solteiro', title=_(u'Solteiro(a)')),
    SimpleTerm(value='casado', title=_(u'Casado(a)')),
    SimpleTerm(value='separado', title=_(u'Separado(a) judicialmente')),
    SimpleTerm(value='divorciado', title=_(u'Divorciado(a)')),
    SimpleTerm(value='viuvo', title=_(u'Viúvo(a)')), ])

enquadramento_options = SimpleVocabulary([
    SimpleTerm(value='Microempreendedor Individual (MEI)', title=_(u'Microempreendedor Individual (MEI)')),
    SimpleTerm(value='Microempresa (ME)', title=_(u'Microempresa (ME)')),
    SimpleTerm(value='Empresas de Pequeno Porte (EPP)', title=_(u'Empresas de Pequeno Porte (EPP)')),
    SimpleTerm(value='Empresário Individual (EI)', title=_(u'Empresário Individual (EI)')),
    SimpleTerm(value='Empresa Individual de Responsabilidade Limitada (EIRELI)', title=_(u'Empresa Individual de Responsabilidade Limitada (EIRELI)')), ])

tipo_societario_options = SimpleVocabulary([
    SimpleTerm(value='Empresário individual', title=_(u'Empresário individual')),
    SimpleTerm(value='Empresa individual de responsabilidade limitada', title=_(u'Empresa individual de responsabilidade limitada')),
    SimpleTerm(value='Sociedade limitada', title=_(u'Sociedade limitada')),
    SimpleTerm(value='Sociedade anônima', title=_(u'Sociedade anônima')),
    SimpleTerm(value='Outro tipo societário', title=_(u'Outro tipo societário')), ])

doenca_grave_options = SimpleVocabulary([
    SimpleTerm(value='Não', title=_(u'Não')),
    SimpleTerm(value='Tuberculose ativa', title=_(u'Tuberculose ativa')),
    SimpleTerm(value='Esclerose múltipla', title=_(u'Esclerose múltipla')),
    SimpleTerm(value='Neoplasia maligna (câncer)', title=_(u'Neoplasia maligna (câncer)')),
    SimpleTerm(value='Hanseníase (Lepra)', title=_(u'Hanseníase (Lepra)')),
    SimpleTerm(value='Paralisia irreversível e incapacitante', title=_(u'Paralisia irreversível e incapacitante')),
    SimpleTerm(value='Cardiopatia grave', title=_(u'Cardiopatia grave')),
    SimpleTerm(value='Doença de Parkinson', title=_(u'Doença de Parkinson')),
    SimpleTerm(value='Espondiloartrose anquilosante', title=_(u'Espondiloartrose anquilosante')),
    SimpleTerm(value='Nefropatia grave', title=_(u'Nefropatia grave')),
    SimpleTerm(value='Hepatopatia grave', title=_(u'Hepatopatia grave')),
    SimpleTerm(value='Doença de Paget (osteíte deformante) em grau avançado', title=_(u'Doença de Paget (osteíte deformante) em grau avançado')),
    SimpleTerm(value='Contaminação por radiação', title=_(u'Contaminação por radiação')),
    SimpleTerm(value='Síndrome de imunodeficiência adquirida (AIDS)', title=_(u'Síndrome de imunodeficiência adquirida (AIDS)')),
    SimpleTerm(value='Outra doença considerada grave por atestado/laudo médico', title=_(u'Outra doença considerada grave por atestado/laudo médico')), ])

adicionais_escolha_um = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

adicionais_escolha_dois = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

adicionais_escolha_tres = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

# termos = SimpleVocabulary([
#     SimpleTerm(value='sim', title=_(u'Eu concordo com os Termos de Uso do Consumidor.'))])


def validateAccept(value):
    if value is not True:
        return False
    return True


class IEnhancedUserDataSchema(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    # termos_uso = schema.List(
    #     title=u"Termos de Uso do Consumidor.",
    #     # description=u"Eu concordo com os Termos de Uso do Consumidor.",
    #     required=False,
    #     value_type=schema.Choice(vocabulary=termos))

    adicional_um = schema.Choice(
        title=_(u'Possui mais de 60 anos ? *'),
        description=_(u'Possui mais de 60 anos ? *'),
        vocabulary=adicionais_escolha_um,
        required=False,)

    adicional_um = schema.Choice(
        title=_(u'Possui mais de 60 anos ? *'),
        description=_(u'Possui mais de 60 anos ? *'),
        vocabulary=adicionais_escolha_um,
        required=False,)

    adicional_tres = schema.Choice(
        title=_(u'Possui alguma deficiência ? *'),
        description=_(u'Possui alguma deficiência ? *'),
        vocabulary=adicionais_escolha_tres,
        required=False,)

    adicional_dois = schema.Choice(
        title=_(u'Portador de alguma doença grave prevista na Lei nº 12.008/09, atestada por declaração/laudo médico ? *'),
        description=_(u'Portador de alguma doença grave prevista na Lei nº 12.008/09, atestada por declaração/laudo médico ? *'),
        vocabulary=adicionais_escolha_dois,
        required=False,)

    doenca_grave = schema.Choice(
        title=_(u'Portador de alguma doença grave, atestada por declaração/laudo médico ? *'),
        description=_(u'Possui alguma deficiência ? *'),
        vocabulary=doenca_grave_options,
        required=False,)

    municipio = schema.Choice(
        title=_(u'Você possui domicílio no Município de São Paulo? *', default=u'Você possui domicílio no Município de São Paulo? *'),
        description=_(u'',
                      default=u""),
        vocabulary=municipio_options,
        required=False,)
    cadastro = schema.Choice(
        title=_(u'Tipo de consumidor *', default=u'Tipo de consumidor *'),
        description=_(u'',
                      default=u""),
        vocabulary=tipo_options,
        required=False,)
    tipo = schema.Choice(
        title=_(u'Tipo de consumidor *', default=u'Tipo de consumidor *'),
        description=_(u'',
                      default=u""),
        vocabulary=tipo_options,
        required=False,)
    nome = schema.TextLine(
        title=_(u'Nome Completo *', default=u'Nome Completo *'),
        description=_(u'',
                      default=u""),
        required=False,)
    razao_social = schema.TextLine(
        title=_(u'Razão social *', default=u'Razão social *'),
        description=_(u'',
                      default=u""),
        required=False,)
    nome_fantasia = schema.TextLine(
        title=_(u'Nome fantasia', default=u'Nome fantasia'),
        description=_(u'',
                      default=u""),
        required=False,)
    deficiencia_especificar = schema.TextLine(
        title=_(u'Especificar', default=u'Especificar'),
        description=_(u'',
                      default=u""),
        required=False,)
    doenca_especificar = schema.TextLine(
        title=_(u'Especificar', default=u'Especificar'),
        description=_(u'',
                      default=u""),
        required=False,)
    responsavel = schema.TextLine(
        title=_(u'Nome completo do representante legal *', default=u'Nome completo do representante legal *'),
        description=_(u'',
                      default=u""),
        required=False,)
    cpf = schema.TextLine(
        title=_(u'CPF *', default=u'CPF *'),
        description=_(u'',
                      default=u""),
        required=False,)
    rg = schema.TextLine(
        title=_(u'RG *', default=u'RG *'),
        description=_(u'',
                      default=u""),
        required=False,)
    expeditor = schema.TextLine(
        title=_(u'Órgão Expedidor *', default=u'Órgão Expedidor *'),
        description=_(u'',
                      default=u""),
        required=False,)
    uf_expedidor = schema.TextLine(
        title=_(u'UF *', default=u'UF *'),
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
                      default=u"Solteiro(a)"),
        vocabulary=estadocivil_options,
        required=False,)
    tipo_societario = schema.Choice(
        title=_(u'Tipo Societário *', default=u'Tipo Societário *'),
        description=_(u'',
                      default=u""),
        vocabulary=tipo_societario_options,
        required=False,)
    enquadramento = schema.Choice(
        title=_(u'Enquadramento *', default=u'Enquadramento *'),
        description=_(u'',
                      default=u""),
        vocabulary=enquadramento_options,
        required=False,)

    data_nascimento = schema.TextLine(
        title=_(u'Data de nascimento', default=u'Data de nascimento'),
        required=False
    )

    contato_telefone = schema.TextLine(
        title=_(u'DDD + Telefone/Celular'),
        required=False
    )

    contato_celular = schema.TextLine(
        title=_(u'DDD + Telefone/Celular'),
        required=False
    )

    codigo_enderecamento_postal = schema.TextLine(
        title=_(u'CEP *', default=u'CEP *'),
        required=False
    )

    logradouro = schema.TextLine(
        title=_(u'Logradouro *'),
        required=False
    )

    complemento = schema.TextLine(
        title=_(u'Número/Complemento *'),
        required=False
    )

    bairro = schema.TextLine(
        title=_(u'Bairro *'),
        required=False
    )

    cidade = schema.TextLine(
        title=_(u'Cidade *'),
        required=False
    )

    unidade_federativa = schema.TextLine(
        title=_(u'UF *'),
        required=False
    )

    site = schema.TextLine(
        title=_(u'Site'),
        required=False
    )

    mail = schema.TextLine(
        title=_(u'E-mail *'),
        required=False
    )

    confirmacao = schema.TextLine(
        title=_(u'Confirmação de E-mail *'),
        required=False
    )


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, UserDataPanel)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields = fields.omit('accept')  # Users have already accepted.
        fields['cadastro'].widgetFactory = RadioFieldWidget
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        fields['adicional_um'].widgetFactory = RadioFieldWidget
        fields['adicional_dois'].widgetFactory = RadioFieldWidget
        fields['adicional_tres'].widgetFactory = RadioFieldWidget
        self.add(fields)


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, RegistrationForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['cadastro'].widgetFactory = RadioFieldWidget
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        fields['adicional_um'].widgetFactory = RadioFieldWidget
        fields['adicional_dois'].widgetFactory = RadioFieldWidget
        fields['adicional_tres'].widgetFactory = RadioFieldWidget
        self.add(fields)


class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, AddUserForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['cadastro'].widgetFactory = RadioFieldWidget
        fields['tipo'].widgetFactory = RadioFieldWidget
        fields['municipio'].widgetFactory = RadioFieldWidget
        fields['genero'].widgetFactory = RadioFieldWidget
        fields['adicional_um'].widgetFactory = RadioFieldWidget
        fields['adicional_dois'].widgetFactory = RadioFieldWidget
        fields['adicional_tres'].widgetFactory = RadioFieldWidget

        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields)

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


uf_options = SimpleVocabulary([
    SimpleTerm(value='SP', title=_(u'SP')),
    SimpleTerm(value='AC', title=_(u'AC')),
    SimpleTerm(value='AL', title=_(u'AL')),
    SimpleTerm(value='AP', title=_(u'AP')),
    SimpleTerm(value='AM', title=_(u'AM')),
    SimpleTerm(value='BA', title=_(u'BA')),
    SimpleTerm(value='CE', title=_(u'CE')),
    SimpleTerm(value='DF', title=_(u'DF')),
    SimpleTerm(value='ES', title=_(u'ES')),
    SimpleTerm(value='GO', title=_(u'GO')),
    SimpleTerm(value='MA', title=_(u'MA')),
    SimpleTerm(value='MT', title=_(u'MT')),
    SimpleTerm(value='MS', title=_(u'MS')),
    SimpleTerm(value='MG', title=_(u'MG')),
    SimpleTerm(value='PA', title=_(u'PA')),
    SimpleTerm(value='PB', title=_(u'PB')),
    SimpleTerm(value='PR', title=_(u'PR')),
    SimpleTerm(value='PE', title=_(u'PE')),
    SimpleTerm(value='PI', title=_(u'PI')),
    SimpleTerm(value='RJ', title=_(u'RJ')),
    SimpleTerm(value='RN', title=_(u'RN')),
    SimpleTerm(value='RS', title=_(u'RS')),
    SimpleTerm(value='RO', title=_(u'RO')),
    SimpleTerm(value='RR', title=_(u'RR')),
    SimpleTerm(value='SC', title=_(u'SC')),
    SimpleTerm(value='SE', title=_(u'SE')),
    SimpleTerm(value='TO', title=_(u'TO')), ])

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
    SimpleTerm(value='Microempreendedor individual - MEI', title=_(u'Microempreendedor individual - MEI')),
    SimpleTerm(value='Microempresa - ME', title=_(u'Microempresa - ME')),
    SimpleTerm(value='Empresa de pequeno porte - EPP', title=_(u'Empresa de pequeno porte - EPP')),
    SimpleTerm(value='Empresa de medio porte', title=_(u'Empresa de médio porte')),
    SimpleTerm(value='Empresa de grande porte', title=_(u'Empresa de grande porte')),
    SimpleTerm(value='Outro', title=_(u'Outro')), ])

tipo_societario_options = SimpleVocabulary([
    SimpleTerm(value='Empresario individual', title=_(u'Empresário individual')),
    SimpleTerm(value='Empresa individual de responsabilidade limitada', title=_(u'Empresa individual de responsabilidade limitada')),
    SimpleTerm(value='Sociedade limitada', title=_(u'Sociedade limitada')),
    SimpleTerm(value='Sociedade anonima', title=_(u'Sociedade anônima')),
    SimpleTerm(value='Outro tipo societario', title=_(u'Outro tipo societário')), ])

doenca_grave_options = SimpleVocabulary([
    SimpleTerm(value='não', title=_(u'Não')),
    SimpleTerm(value='Tuberculose ativa', title=_(u'Tuberculose ativa')),
    SimpleTerm(value='Esclerose múltipla', title=_(u'Esclerose múltipla')),
    SimpleTerm(value='Neoplasia maligna - câncer', title=_(u'Neoplasia maligna (câncer)')),
    SimpleTerm(value='Hanseniase - Lepra', title=_(u'Hanseníase (Lepra)')),
    SimpleTerm(value='Paralisia irreversivel e incapacitante', title=_(u'Paralisia irreversível e incapacitante')),
    SimpleTerm(value='Cardiopatia grave', title=_(u'Cardiopatia grave')),
    SimpleTerm(value='Doenca de Parkinson', title=_(u'Doença de Parkinson')),
    SimpleTerm(value='Espondiloartrose anquilosante', title=_(u'Espondiloartrose anquilosante')),
    SimpleTerm(value='Nefropatia grave', title=_(u'Nefropatia grave')),
    SimpleTerm(value='Hepatopatia grave', title=_(u'Hepatopatia grave')),
    SimpleTerm(value='Doenca de Paget - osteite deformante - em grau avançado', title=_(u'Doença de Paget (osteíte deformante) em grau avançado')),
    SimpleTerm(value='Contaminacao por radiacao', title=_(u'Contaminação por radiação')),
    SimpleTerm(value='Síndrome de imunodeficiencia adquirida - AIDS', title=_(u'Síndrome de imunodeficiência adquirida (AIDS)')),
    SimpleTerm(value='Outra doença considerada grave por atestado - laudo médico', title=_(u'Outra doença considerada grave por atestado/laudo médico')), ])

adicionais_escolha_um = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])

adicionais_escolha_dois = SimpleVocabulary([
    SimpleTerm(value='sim', title=_(u'Sim')),
    SimpleTerm(value='nao', title=_(u'Não')), ])


adicionais_campo_escolha_tres = SimpleVocabulary([
    SimpleTerm(value='não', title=_(u'Não')),
    SimpleTerm(value='Deficiencia Visual', title=_(u'Deficiência Visual')),
    SimpleTerm(value='Deficiencia Auditiva - Surdez', title=_(u'Deficiência Auditiva/Surdez')),
    SimpleTerm(value='Deficiencia intelectual', title=_(u'Deficiência intelectual')),
    SimpleTerm(value='Deficiencia fisica', title=_(u'Deficiência física')),
    SimpleTerm(value='Transtorno do Espectro Autista - Lei n 12.764 12', title=_(u'Transtorno do Espectro Autista - Lei nº 12.764/12')),
    SimpleTerm(value='Surdocegueira', title=_(u'Surdocegueira')), ])


adicionais_escolha_tres = SimpleVocabulary([
    SimpleTerm(value='Não', title=_(u'Não')),
    SimpleTerm(value='Deficiência Visual', title=_(u'Deficiência Visual')),
    SimpleTerm(value='Deficiência Auditiva/Surdez ', title=_(u'Deficiência Auditiva/Surdez ')),
    SimpleTerm(value='Deficiência intelectual', title=_(u'Deficiência intelectual')),
    SimpleTerm(value='Deficiência física', title=_(u'Deficiência física')),
    SimpleTerm(value='Transtorno do Espectro Autista - Lei nº 12.764/12', title=_(u'Transtorno do Espectro Autista - Lei nº 12.764/12')),
    SimpleTerm(value='Surdocegueira', title=_(u'Surdocegueira')), ])

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

    campo_adicional_um = schema.Choice(
        title=_(u'Possui mais de 60 anos ? *'),
        description=_(u'Possui mais de 60 anos ? *'),
        vocabulary=adicionais_escolha_um,
        required=False,)

    adicional_um = schema.Choice(
        title=_(u'Possui mais de 60 anos ? *'),
        description=_(u'Possui mais de 60 anos ? *'),
        vocabulary=adicionais_escolha_um,
        required=False,)

    campo_adicional_tres = schema.Choice(
        title=_(u'Possui alguma deficiência? *'),
        description=_(u'Possui alguma deficiência? *'),
        vocabulary=adicionais_campo_escolha_tres,
        required=False,)

    campoadicional_tres = schema.Choice(
        title=_(u'Possui alguma deficiência? *'),
        description=_(u'Possui alguma deficiência? *'),
        vocabulary=adicionais_campo_escolha_tres,
        required=False,)

    adicional_tres = schema.Choice(
        title=_(u'Possui alguma deficiência? *'),
        description=_(u'Possui alguma deficiência? *'),
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

    campo_doenca_grave = schema.Choice(
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

    uf_estados = schema.Choice(
        title=_(u'UF *', default=u'UF *'),
        description=_(u'',
                      default=u"Solteiro(a)"),
        vocabulary=uf_options,
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
        title=_(u'DDD + Telefone/Celular *'),
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

        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields)

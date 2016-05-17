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


def validateAccept(value):
    if value is not True:
        return False
    return True


class IEnhancedUserDataSchema(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """
    tipo = schema.Choice(
        title=_(u'', default=u''),
        description=_(u'',
                      default=u""),
        vocabulary=tipo_options,
        required=False,)
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


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, UserDataPanel)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields = fields.omit('accept')  # Users have already accepted.
        fields['tipo'].widgetFactory = RadioFieldWidget
        self.add(fields)


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, RegistrationForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['tipo'].widgetFactory = RadioFieldWidget
        self.add(fields)


class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IProdamPortal, AddUserForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields['tipo'].widgetFactory = RadioFieldWidget
        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields)

# -*- coding: utf-8 -*-

from plone.app.users.browser.passwordpanel import PasswordPanel
from z3c.form import button
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
# from plone.app.users.browser.passwordpanel import PasswordPanelAdapter


class PasswordPanel(PasswordPanel):

    @button.buttonAndHandler(
        _(u'label_change_password', default=u'Change Password'),
        name='reset_passwd'
    )
    def action_reset_passwd(self, action):
        data, errors = self.extractData()

        # extra password validation
        self.validate_password(action, data)

        if action.form.widgets.errors:
            self.status = self.formErrorsMessage
            return

        membertool = getToolByName(self.context, 'portal_membership')

        password = data['new_password']

        try:
            membertool.setPassword(password, None, REQUEST=self.request)
        except AttributeError:
            failMessage = _(u'While changing your password an AttributeError '
                            u'occurred. This is usually caused by your user '
                            u'being defined outside the portal.')

            IStatusMessage(self.request).addStatusMessage(
                _(failMessage), type="error"
            )
            return
        self.request.response.redirect(self.context.portal_url() + '/senha_alterada')

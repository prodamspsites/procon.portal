# -*- coding: utf-8 -*-
from collective.transmogrifier.transmogrifier import configuration_registry
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Instala produtos
        z2.installProduct(app, 'Products.PloneFormGen')
        # Load ZCML
        import procon.portal
        self.loadZCML(package=procon.portal)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'procon.portal:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

    def tearDown(self):
        super(Fixture, self).tearDown()
        configuration_registry.clear()

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='procon.portal:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='procon.portal:Functional',
)

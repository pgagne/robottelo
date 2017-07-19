"""Test for virt-who configure UI

:Requirement: Virtwho-configure

:CaseLevel: Acceptance

:CaseComponent: UI

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""

from robottelo.decorators import run_only_on, stubbed, tier1, tier2, tier3
from robottelo.test import UITestCase, TestCase


class VirtWhoConfigUITestCase(UITestCase):
    """Implements Virt-who-configure tests in UI"""

    @run_only_on('sat')
    @stubbed()
    @tier1
    def test_postive_config_page_populated(self):
        """DESCRIPTION

        :id: db6bbc68-2047-4c7d-af5b-31aee0030318

        :setup: 

        :steps:
            1. 


        :expectedresults: 

        :Caseautomation: notautomated

        :CaseImportance: Critical
        """

    def test_postive_config_page_empty(self):
        """
        2
         
        """
        pass

    def test_postive_dashboard_no_reports(self):
        pass

    def test_postive_dashboard_out_of_date(self):
        pass

    def test_postive_dashboard_up_to_date(self):
        pass

    def test_postive_lastest_out_of_date(self):
        pass

    def test_postive_vm_create(self):
        pass


class VirtWhoConfigCLITestCase(UITestCase):
    pass


class VirtWhoConfigEndToEnd(TestCase):

    def test_positive_libvirt(self):
        pass


    def test_positive_rhev(self):
        pass

    def test_positive_rhv(self):
        pass

    def test_positive_hyperv(self):
        pass

    def test_positive_xen(self):
        pass






"""Test for virt-who configure UI

:Requirement: Virtwho-configure

:CaseLevel: Acceptance

:CaseComponent: UI

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""

from robottelo.decorators import run_only_on, stubbed, tier1, tier2, tier3
from robottelo.test import UITestCase, TestCase, APITestCase


class VirtWhoConfigUITestCase(UITestCase):
    """Implements Virt-who-configure tests in UI"""

    @run_only_on('sat')
    @stubbed()
    @tier1
    def test_positive_config_page_populated(self):
        """DESCRIPTION

        :id: db6bbc68-2047-4c7d-af5b-31aee0030318

        :setup: 

        :steps:
            1. 


        :expectedresults: 

        :Caseautomation: notautomated

        :CaseImportance: Critical
        """

    def test_positive_config_page_empty(self):
        """
        2
         
        """
        pass

    def test_positive_dashboard_no_reports(self):
        pass

    def test_positive_dashboard_out_of_date(self):
        pass

    def test_positive_dashboard_up_to_date(self):
        pass

    def test_positive_lastest_out_of_date(self):
        pass

    def test_positive_vm_create(self):
        pass

    def test_negative_vm_create(self):
        pass

    def test_positive_config_update(self):
        pass

    def test_negative_config_update(self):
        pass


class VirtWhoConfigRoleApiTests(APITestCase):
    
    def test_positive_role_manager(self):
        """virt-who Manager
        a. Create a user with ONLY the virt-who manager role.
        b. Verify the user can create virt-who configurations
        c. Verify the user can edit an existing virt-who configuration
        d. Verify the user can delete a virt-who configuration
        e. Verify the user can see virt-who reporting information through the dashboard
        f. Verify the user can do no other actions
        :return:
        """
        pass
    
    def test_negative_role_manager(self):
        """
        f. Verify the user can do no other actions

        :return:
        """
        pass

    def test_positive_role_reporter(self):
        """
        2. virt-who Reporter
        a. Create a user with ONLY the virt-who reporter role.
        b. Configure virt-who WITHOUT using the virt-who config plugin. Set the Satellite the created user.
        c. Create a vm to cause virt-who to send a report to satellite.
        d. Verify the virt-who server send a report to the satellite.
        """
        pass

    def test_negative_role_reporter(self):
        """
                e. Verify the user can do no other actions

        :return:
        """
        pass

    def test_positive_role_viewer(self):
        """
        3. virt-who Viewer
        a. Create a user with ONLY the virt-who Viewer role.
        b. Verify the user can view virt-who configurations.
        c. Verify the user CANNOT delete or modify virt-who configurations
        """
        pass

    def test_negative_role_viewer(self):
        """
        d. Verify the user can do no other actions

        :return:
        """
        pass



class VirtWhoConfigUpgrade(UITestCase):

    def test_positive_satellite_upgrade(self):
        """ Satellite upgrade

        :uuid: 0e301c08-8bef-4bea-a690-d4b0760949e8

        :Steps:

        1. Start with a satellite version before the virt-who configurator plugin
        2. Configure a virt-who server with virtualization provider (VP1) to send reports to the satellite.
        3. Upgrade the satellite to a version with virt-who configurator plugin.
        4. Configure a new virtualization provider (VP2)  with a VDC subscription
        5. Using the virt-who plugin, create a configuration for the new hypervisor.
        6. Deploy the configuration to the virt-who server
        7. Create a guest on VP1
        8. Create a guest on VP2
        9. verify that that reports on VP1 and VP2 are correct.
        """








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






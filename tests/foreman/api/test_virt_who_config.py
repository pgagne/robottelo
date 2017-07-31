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
    """Implements Virt-who-configure UI tests"""

    def test_positive_welcome_page(self):
        """
        1. Verify welcome page

        :return:
        """

    def test_positive_configurations_page(self):
        """
        1. Create virt-who-configurations
        2. Verify the new virt-who Configurations UI (the page which lists all virt-who configurations)

        """
        pass

    def test_positive_shell_script_display(self):
        pass

    def test_postitve_config_change_redeploy(self):
        """
        13.  Edit virt-who configuration and verify the updated shell script, redeploy the script
        """



    def test_negative_virt_who_user_login(self):
        """
        17. Make sure the users created by virt-who config is not able to access UI/CLI
        1. Create a virt-who configuration
        2. Attempt to login the UI with the user created by the virt-who configurator. Verify the login is blocked
        3. Attempt to login using Hammer with the user created by the virt-who configurator. Verify the login is blocked
        4. Attempt to click the username link displayed in related task details.
        :return:
        """

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
class VirtWhoConfigAPI(APITestCase):
    def test_positive_vm_create(self):
        """
        8. Create new VM in a supported hypervisor and check if it is reported to Satellite (waiting until the next virt-who report comes in)

        :return:
        """
        pass

    def test_negative_vm_create(self):
        """
        9. Check if there are no virt-who reports reported if there is no change in guest-host mapping in hypervisor

        :return:
        """
        pass

    def test_positive_config_update(self):
        pass

    def test_negative_config_update(self):
        pass

    def test_postive_config_intervals(self):
        """ Intervals
        1. Create a virt-who configuration with a reporting interval of every 1 hour.
        2. Verify a Virt-who configuration is created that sets the interval to 1 hour
        3. Verify a report is sent every hour
        4. Repeat for each supported interval.

        :return:
        """
        pass

class VirtWhoConfigDashboardUITestCase(UITestCase):
    """
    6. Review UI Dashboard
        - No reports
        - Out of Date
        - Up to Date
        - Latest out of date Configurations

    """

    def test_positive_dashboard_no_reports(self):
        """
        - No reports

        """
        pass

    def test_positive_dashboard_out_of_date(self):
        """
        - Out of Date

        :return:
        """
        pass

    def test_positive_dashboard_up_to_date(self):
        """
        - Up to Date
        :return:
        """
        pass

    def test_positive_lastest_out_of_date(self):
        """
        - Latest out of date Configurations
        :return:
        """





class VirtWhoConfigRoleApiTests(APITestCase):
    
    def test_positive_role_manager(self):
        """virt-who Manager
        1. Create a user with ONLY the virt-who manager role.
        2. Verify the user can create virt-who configurations
        3. Verify the user can edit an existing virt-who configuration
        4. Verify the user can delete a virt-who configuration
        5. Verify the user can see virt-who reporting information through the dashboard
        6. Verify the user can do no other actions
        :return:
        """
        pass
    
    def test_negative_role_manager(self):
        """
        1. Verify the user can do no other actions

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



class VirtWhoConfigUpgrade(APITestCase):

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








class VirtWhoConfigCLITestCase():
    def test_positive_create_cli_deploy_ui(self):
        """Verify  “hammer virt-who-config”
            1. Create config in UI, deploy using “hammer virt-who-config deploy”
        :return:
        """

    def test_positive_create_cli_deploy_cli(self):
        """
        2. Create config using hammer, deploy using hammer.
        """
    pass

    def test_negative_virt_who_user_login(self):
        """
        17. Make sure the users created by virt-who config is not able to access UI/CLI
        1. Create a virt-who configuration
        2. Attempt to login the UI with the user created by the virt-who configurator. Verify the login is blocked
        3. Attempt to login using Hammer with the user created by the virt-who configurator. Verify the login is blocked
        4. Attempt to click the username link displayed in related task details.
        :return:
        """




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

class VirtWhoConfigGeneralTestcase(TestCase):
    def test_positive_multiple_config_single_instance(self):
        """ Create multiple configs, add to same virt-who instance
        1. Create a virt-who config (VHCONFIG1) for VMware
        2. Create a virt-who config (VHCONFIG2) for RHV
        3. Deploy VHCONFIG1 and VHCONFIG2 to the same virt-who server
        4. Create guests on the VMware and RHV hypervisors
        5. Verify the correct information is reported to the Satellite.
        """

    def test_positive_multiple_config_same_instance(self):
        """Create multiple configs for multiple virt-who instances
                1. Create a virt-who config (VHCONFIG1) for VMware
                2. Create a virt-who config (VHCONFIG2) for RHV
                3. Deploy VHCONFIG1 and VHCONFIG2 to the 2 different virt-who server
                4. Create guests on the VMware and RHV hypervisors
                5. Verify the correct information is reported to the Satellite.


        """

    def test_positive_delete_config_delete_user(self):
        """Verify when a config is deleted the associated user is deleted.
                1. Create a virt-who configuration and deploy it to a virt-who server.
                2. Delete the configuration on the Satellite.
                3. Verify the virt-who server can no longer send reports to the Satellite.

        """

    def test_positive_register_user_password(self):
        """Register guest with username/password
                1. Create a virt-who configuration for a hypervisor
                2. Create a guest on a hypervisor.
                3. Attempt to register the guest using the admin username/password .
                4. Create a user with a content host registration role (REGUSER)
                5. Verify a guest can be registered using the REGUSER user.

        """







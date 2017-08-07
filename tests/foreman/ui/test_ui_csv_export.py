"""Test for UI CSV EXPORT

:Requirement: Virtwho-configure

:CaseLevel: Acceptance

:CaseComponent: UI

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""

from robottelo.decorators import run_only_on, stubbed, tier1, tier2, tier3
from robottelo.test import UITestCase


class UICSVExportHosts(UITestCase):


    @stubbed
    @tier1
    def test_positive_single_page(self):
        """
        :id: be5e2b2d-3a93-4803-8c6e-d81a97c5a1a5

        :step
        """
    @stubbed
    @tier1
    def test_positive_multi_page(self):
        """
        :id: cb615ed3-2f4c-45b5-904e-890ccb587842

        :steps:
            1. Populate page with >20 (or max# per-page) items. For example 30
            2. Press export CSV button

        :expectedresult: Exported CSV will have all rows (30)

        """

    @tier1
    def test_positive_organization_filter(self):
        """
        :id: 76756510-eaf1-48be-bd87-8f218c5378cb
        :return:
        """

    def test_negative_organization_filter(self):
        pass

    def test_positive_location_filter(self):
        pass

    def test_negative_location_filter(self):
        pass

    def test_combo_filter(self):
        pass

    def test_positive_filter_multi_page(self):
        pass

    def test_positive_filter_single_page(self):
        pass


class UICSVExportHostsColumns(UITestCase):

    def test_positive_column_contents(self):
        """
        :setup:
            Populate hosts multiple hosts with a mix of Puppet Enviromets, Hostgroups, OS, etc
        :steps:
            1. Export the CSV Page in the UI

        :expectedresults: Exported CSV will contain text representations of all columns.

        :return:
        """

    def test_positive_name(self):
        pass

    def test_positive_os(self):
        pass


    def test_positive_enviroment(self):
        pass

    def test_negative_enviroment(self):
        pass

    def test_positive_model_baremetal(self):
        pass

    def test_positive_compute_resource(self):
        pass

    def test_positive_last_report(self):
        pass

    def test_negative_last_report(self):
        """
        test entry with no last report time
        :return:
        """
        pass

class UICSVExportFacts(UITestCase):

    def test_positive_single_page(self):
        pass

    def test_positive_multipage(self):
        """
        :id: cb615ed3-2f4c-45b5-904e-890ccb587842

        :setup:
            1. Populate page with >20 (or max# per-page) items. For example 30

        :steps:

            2. Press export CSV button

        :expectedresult: Exported CSV will have all rows (30)

        """

        def test_positive_organization_filter(self):
            """
            :s
            :return:
            """

        def test_negative_organization_filter(self):
            pass

        def test_positive_location_filter(self):
            pass

        def test_negative_location_filter(self):
            pass

        def test_combo_filter(self):
            pass

        def test_positive_filter_multi_page(self):
            pass

        def test_positive_filter_single_page(self):
            pass

        def test_positive_nested_facts(self):
            """
            Recurse down a nested fact list
            :param self:
            :return:
            """

class UICSVExportFactsColumns(UITestCase):

    def setUp(self):
        pass

    def test_positive_name(self):
        pass

    def test_positive_value(self):
        pass

    def test_positive_origin(self):
        pass

    def test_positive_reported(self):
        pass

    def test_postive_nested_value(self):
        """
        Verify what ever the end result of https://bugzilla.redhat.com/show_bug.cgi?id=1477341 is.

        :return:
        """
        pass



class UICSVExportFactsNested(UITestCase):
    pass

class UICSVExportConfigMgmtReports(UITestCase):
    pass





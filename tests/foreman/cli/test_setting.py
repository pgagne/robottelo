# -*- encoding: utf-8 -*-
"""Test class for Setting Parameter values

:Requirement: Setting

:CaseAutomation: Automated

:CaseLevel: Acceptance

:CaseComponent: CLI

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
import pytest

from robottelo.cli.base import CLIReturnCodeError
from robottelo.cli.settings import Settings
from robottelo.datafactory import (
    gen_string,
    generate_strings_list,
    invalid_boolean_strings,
    invalid_emails_list,
    valid_data_list,
    valid_emails_list,
    valid_url_list,
    xdist_adapter
)
from robottelo.decorators import stubbed, tier1
from robottelo.test import CLITestCase


class SettingTestCase(CLITestCase):
    """Implements tests for Settings for CLI"""

    @classmethod
    def setUpClass(cls):
        super(SettingTestCase, cls).setUpClass()
        # Collect original defaults so we can reset them later
        cls.default_settings = {k['name']: k['value'] for k in Settings.list()}

    def setUp(self):
        self.reset_settings = set()

    def tearDown(self):
        # Reset settings to defaults
        for s in self.reset_settings:
            Settings.set({'name': s, 'value': self.default_settings[s]})

    def setSetting(self, name, value):
        """
        Wrapper around Settings.set to help us ensure settings are reset to
        default values

        :param name: Name of the setting to set
        :param value: value to set
        :return: None
        """
        self.reset_settings.add(name)
        Settings.set({'name': name, 'value': value})

    @stubbed()
    @tier1
    def test_negative_update_hostname_with_empty_fact(self):
        """Update the Hostname_facts settings without any string(empty values)

        :id: daca0746-75ad-42fb-97ed-6db0224eeeac

        :expectedresults: Error should be raised on setting empty value for
            hostname_facts setting

        :caseautomation: notautomated
        """

    @tier1
    def test_positive_update_hostname_prefix_without_value(self):
        """Update the Hostname_prefix settings without any string(empty values)

        :id: a84c28ea-6821-4c31-b4ab-8662c22c9135

        :expectedresults: Hostname_prefix should be set without any text
        """
        self.setSetting("discovery_prefix", "")
        discovery_prefix = Settings.list({
            'search': 'name=discovery_prefix'
        })[0]
        self.assertEqual('', discovery_prefix['value'])

    @tier1
    def test_positive_update_hostname_default_prefix(self):
        """Update the default set prefix of hostname_prefix setting

        :id: a6e46e53-6273-406a-8009-f184d9551d66

        :expectedresults: Default set prefix should be updated with new value
        """
        hostname_prefix_value = gen_string('alpha')
        self.setSetting("discovery_prefix", hostname_prefix_value)
        discovery_prefix = Settings.list({
            'search': 'name=discovery_prefix'
        })[0]
        self.assertEqual(hostname_prefix_value, discovery_prefix['value'])

    @stubbed()
    @tier1
    def test_positive_update_hostname_default_facts(self):
        """Update the default set fact of hostname_facts setting with list of
        facts like: bios_vendor,uuid

        :id: 1042c5e2-ee4d-4eaf-a0b2-86c000a79dfb

        :expectedresults: Default set fact should be updated with facts list.

        :caseautomation: notautomated
        """

    @stubbed()
    @tier1
    def test_negative_discover_host_with_invalid_prefix(self):
        """Update the hostname_prefix with invalid string like
        -mac, 1mac or ^%$

        :id: 73c5da42-28c8-4be7-8fb1-f505fefd6665

        :expectedresults: Validation error should be raised on updating
            hostname_prefix with invalid string, should start w/ letter

        :caseautomation: notautomated
        """

    @tier1
    def test_positive_update_login_page_footer_text(self):
        """Updates parameter "login_text" in settings

        :id: 4d4e1151-5bd6-4fa2-8dbb-e182b43ad7ec

        :steps:

            1. Execute "settings" command with "set" as sub-command
            with any string

        :expectedresults: Parameter is updated successfully
        """
        for login_text_value in valid_data_list():
            with self.subTest(login_text_value):
                self.setSetting("login_text", login_text_value)
                login_text = Settings.list({'search': 'name=login_text'})[0]
                self.assertEqual(login_text_value, login_text['value'])

    @tier1
    def test_positive_update_login_page_footer_text_without_value(self):
        """Updates parameter "login_text" without any string (empty value)

        :id: 01ce95de-2994-42b6-b9f8-f7882981fb69

        :steps:

            1. Execute "settings" command with "set" as sub-command
            without any string(empty value) in value parameter

        :expectedresults: Message on login screen should be removed
        """
        self.setSetting('login_text', '')
        login_text = Settings.list({'search': 'name=login_text'})[0]
        self.assertEqual('', login_text['value'])

    @tier1
    def test_positive_update_login_page_footer_text_with_long_string(self):
        """Attempt to update parameter "Login_page_footer_text"
            with long length string under General tab

        :id: 87ef6b19-fdc5-4541-aba8-e730f1a3caa7

        :steps:
            1. Execute "settings" command with "set" as sub-command
            with long length string

        :expectedresults: Parameter is updated

        :caseimportance: low
        """
        for login_text_value in generate_strings_list(1000):
            with self.subTest(login_text_value):
                Settings.set({'name': "login_text", 'value': login_text_value})
                login_text = Settings.list({'search': 'name=login_text'})[0]
                self.assertEqual(login_text_value, login_text['value'])

    @stubbed()
    @tier1
    def test_positive_update_email_delivery_method_smtp(self):
        """Check Updating SMTP params through settings subcommand

        :id: b26798e9-528c-4ed6-a09b-dc8e4668a8d7

        :steps:
            1. set "delivery_method" to smtp
            2. set all smtp related properties:
                2.1. smtp_address
                2.2. smtp_authentication
                2.3. smtp_domain
                2.4. smtp_enable_starttls_auto
                2.5. smtp_openssl_verify_mode
                2.6. smtp_password
                2.7. smtp_port
                2.8. smtp_user_name

        :expectedresults: SMTP properties are updated

        :caseimportance: low

        :caseautomation: notautomated
        """

    @stubbed()
    @tier1
    def test_positive_update_email_delivery_method_sendmail(self):
        """Check Updating Sendmail params through settings subcommand

        :id: 578de898-fde2-4957-b39a-9dd059f490bf

        :steps:
            1. set "delivery_method" to sendmail
            2. set all sendmail related properties:
                2.1. sendmail_arguments
                2.2. sendmail_location

        :expectedresults: Sendmail properties are updated

        :caseimportance: low

        :caseautomation: notautomated
        """

    @tier1
    def test_positive_update_email_reply_address(self):
        """Check email reply address is updated

        :id: cb0907d1-9cb6-45c4-b2bb-e2790ea55f16

        :expectedresults: email_reply_address is updated

        :caseimportance: low

        :caseautomation: automated
        """
        for email in valid_emails_list():
            with self.subTest(email):
                # The email must be escaped because some characters to not fail
                # the parsing of the generated shell command
                escaped_email = email.replace(
                    '"', r'\"').replace('`', r'\`')
                self.setSetting('email_reply_address', escaped_email)
                email_reply_address = Settings.list({
                    'search': 'name=email_reply_address'
                }, output_format='json')[0]
                self.assertEqual(email_reply_address['value'], email)

    @tier1
    def test_negative_update_email_reply_address(self):
        """Check email reply address is not updated

        :id: 2a2220c2-badf-47d5-ba3f-e6329930ab39

        :steps: provide invalid email addresses

        :expectedresults: email_reply_address is not updated

        :caseimportance: low

        :caseautomation: automated
        """
        for email in invalid_emails_list():
            with self.subTest(email):
                with self.assertRaises(CLIReturnCodeError):
                    self.setSetting('email_reply_address', email)

    @tier1
    def test_positive_update_email_subject_prefix(self):
        """Check email subject prefix is updated

        :id: c8e6b323-7b39-43d6-a9f1-5474f920bba2

        :expectedresults: email_subject_prefix is updated

        :caseautomation: automated

        :caseimportance: low
        """
        email_subject_prefix_value = gen_string('alpha')
        self.setSetting('email_subject_prefix', email_subject_prefix_value)
        email_subject_prefix = Settings.list({
            'search': 'name=email_subject_prefix'
        })[0]
        self.assertEqual(
            email_subject_prefix_value,
            email_subject_prefix['value']
        )

    @stubbed()
    @tier1
    def test_negative_update_email_subject_prefix(self):
        """Check email subject prefix not

        :id: 8a638596-248f-4196-af36-ad2982196382

        :steps: provide invalid prefix, like string with more than 255 chars

        :expectedresults: email_subject_prefix is not updated

        :caseautomation: notautomated

        :caseimportance: low
        """

    @tier1
    def test_positive_update_send_welcome_email(self):
        """Check email send welcome email is updated

        :id: cdaf6cd0-5eea-4252-87c5-f9ec3ba79ac1

        :steps: valid values: boolean true or false

        :expectedresults: send_welcome_email is updated

        :caseautomation: automated

        :caseimportance: low
        """
        for value in ['true', 'false']:
            self.setSetting('send_welcome_email', value)
            host_value = Settings.list(
              {'search': 'name=send_welcome_email'})[0]['value']
            assert value == host_value

    @tier1
    def test_positive_enable_disable_rssfeed(self):
        """Check if the RSS feed can be enabled or disabled

        :id: 021cefab-2629-44e2-a30d-49c944d0a234

        :steps: Set rss_enable true or false

        :expectedresults: rss_enable is updated

        :caseautomation: automated
        """
        for value in ['true', 'false']:
            self.setSetting('rss_enable', value)
            rss_setting = Settings.list({'search': 'name=rss_enable'})[0]
            self.assertEqual(value, rss_setting['value'])

    @tier1
    def test_positive_update_rssfeed_url(self):
        """Check if the RSS feed URL is updated

        :id: 166ff6f2-e36e-4934-951f-b947139d0d73

        :steps:
            1. Save the original RSS URL
            2. Update RSS feed with a valid URL
            3. Assert the RSS feed URL was really updated
            4. Restore the original feed URL

        :expectedresults: RSS feed URL is updated

        :caseautomation: automated
        """
        for test_url in valid_url_list():
            self.setSetting('rss_url', test_url)
            updated_url = Settings.list({'search': 'name=rss_url'})[0]
            self.assertEqual(test_url, updated_url['value'])


@pytest.mark.parametrize('value', **xdist_adapter(invalid_boolean_strings()))
@tier1
def test_negative_update_send_welcome_email(value):
    """Check email send welcome email is updated

    :id: 2f75775d-72a1-4b2f-86c2-98c36e446099

    :steps: set invalid values: not booleans

    :expectedresults: send_welcome_email is not updated

    :caseautomation: automated

    :caseimportance: low
    """
    with pytest.raises(CLIReturnCodeError):
        Settings.set({'name': 'send_welcome_email', 'value': value})

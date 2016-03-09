"""CLI tests for ``hammer host``."""
from fauxfactory import gen_mac, gen_string
from nailgun import entities
from robottelo.cli.base import CLIReturnCodeError
from robottelo.cli.factory import (
    make_activation_key,
    make_architecture,
    make_content_view,
    make_domain,
    make_environment,
    make_lifecycle_environment,
    make_medium,
    make_org,
    make_os,
    setup_org_for_a_custom_repo,
    setup_org_for_a_rh_repo,
)
from robottelo.cli.host import Host
from robottelo.cli.medium import Medium
from robottelo.cli.operatingsys import OperatingSys
from robottelo.cli.proxy import Proxy
from robottelo.config import settings
from robottelo.constants import (
    FAKE_0_CUSTOM_PACKAGE,
    FAKE_0_CUSTOM_PACKAGE_GROUP,
    FAKE_0_CUSTOM_PACKAGE_GROUP_NAME,
    FAKE_0_CUSTOM_PACKAGE_NAME,
    FAKE_1_CUSTOM_PACKAGE,
    FAKE_1_CUSTOM_PACKAGE_NAME,
    FAKE_2_CUSTOM_PACKAGE,
    FAKE_0_ERRATA_ID,
    FAKE_0_YUM_REPO,
    PRDS,
    REPOS,
    REPOSET,
)
from robottelo.datafactory import (
    invalid_values_list,
    valid_data_list,
    valid_hosts_list,
)
from robottelo.decorators import (
    run_only_on,
    skip_if_not_set,
    tier1,
    tier2,
    tier3,
)
from robottelo.test import CLITestCase
from robottelo.vm import VirtualMachine


class HostCreateTestCase(CLITestCase):
    """Tests for creating the hosts via CLI."""

    def setUp(self):
        """Find an existing puppet proxy.

        Record information about this puppet proxy as ``self.puppet_proxy``.
        """
        super(HostCreateTestCase, self).setUp()
        # Use the default installation smart proxy
        result = Proxy.list()
        self.assertGreater(len(result), 0)
        self.puppet_proxy = result[0]

    @tier1
    def test_positive_create_with_name(self):
        """A host can be created with a random name

        @feature: Hosts

        @assert: A host is created and the name matches
        """
        for name in valid_hosts_list():
            with self.subTest(name):
                host = entities.Host()
                host.create_missing()
                result = Host.create({
                    u'architecture-id': host.architecture.id,
                    u'domain-id': host.domain.id,
                    u'environment-id': host.environment.id,
                    # pylint:disable=no-member
                    u'location-id': host.location.id,
                    u'mac': host.mac,
                    u'medium-id': host.medium.id,
                    u'name': name,
                    u'operatingsystem-id': host.operatingsystem.id,
                    # pylint:disable=no-member
                    u'organization-id': host.organization.id,
                    u'partition-table-id': host.ptable.id,
                    u'puppet-proxy-id': self.puppet_proxy['id'],
                    u'root-pass': host.root_pass,
                })
                self.assertEqual(
                    '{0}.{1}'.format(name, host.domain.read().name).lower(),
                    result['name'],
                )

    @skip_if_not_set('compute_resources')
    @tier1
    def test_positive_create_using_libvirt_without_mac(self):
        """Create a libvirt host and not specify a MAC address.

        @Feature: Hosts

        @Assert: Host is created
        """
        compute_resource = entities.LibvirtComputeResource(
            url='qemu+ssh://root@{0}/system'.format(
                settings.compute_resources.libvirt_hostname
            )
        ).create()
        host = entities.Host()
        host.create_missing()
        result = Host.create({
            u'architecture-id': host.architecture.id,
            u'compute-resource-id': compute_resource.id,
            u'domain-id': host.domain.id,
            u'environment-id': host.environment.id,
            u'interface': 'type=network',
            u'location-id': host.location.id,  # pylint:disable=no-member
            u'medium-id': host.medium.id,
            u'name': host.name,
            u'operatingsystem-id': host.operatingsystem.id,
            # pylint:disable=no-member
            u'organization-id': host.organization.id,
            u'partition-table-id': host.ptable.id,
            u'puppet-proxy-id': self.puppet_proxy['id'],
            u'root-pass': host.root_pass,
        })
        self.assertEqual(result['name'], host.name + '.' + host.domain.name)
        Host.delete({'id': result['id']})


class HostDeleteTestCase(CLITestCase):
    """Tests for deleting the hosts via CLI."""

    def setUp(self):
        """Create a host to use in tests"""
        super(HostDeleteTestCase, self).setUp()
        # Use the default installation smart proxy
        result = Proxy.list()
        self.assertGreater(len(result), 0)
        self.puppet_proxy = result[0]
        self.host = entities.Host()
        self.host.create_missing()
        self.host = Host.create({
            u'architecture-id': self.host.architecture.id,
            u'domain-id': self.host.domain.id,
            u'environment-id': self.host.environment.id,
            # pylint:disable=no-member
            u'location-id': self.host.location.id,
            u'mac': self.host.mac,
            u'medium-id': self.host.medium.id,
            u'name': gen_string('alphanumeric'),
            u'operatingsystem-id': self.host.operatingsystem.id,
            # pylint:disable=no-member
            u'organization-id': self.host.organization.id,
            u'partition-table-id': self.host.ptable.id,
            u'puppet-proxy-id': self.puppet_proxy['id'],
            u'root-pass': self.host.root_pass,
        })

    @tier1
    def test_positive_delete_by_id(self):
        """Create a host and then delete it by id.

        @Feature: Hosts

        @Assert: Host is deleted
        """
        Host.delete({'id': self.host['id']})
        with self.assertRaises(CLIReturnCodeError):
            Host.info({'id': self.host['id']})

    @tier1
    def test_positive_delete_by_name(self):
        """Create a host and then delete it by name.

        @Feature: Hosts

        @Assert: Host is deleted
        """
        Host.delete({'name': self.host['name']})
        with self.assertRaises(CLIReturnCodeError):
            Host.info({'name': self.host['name']})


class HostUpdateTestCase(CLITestCase):
    """Tests for updating the hosts."""

    def setUp(self):
        """Create a host to reuse later"""
        super(HostUpdateTestCase, self).setUp()
        self.proxies = Proxy.list()
        self.assertGreater(len(self.proxies), 0)
        self.puppet_proxy = self.proxies[0]
        # using nailgun to create dependencies
        self.host_args = entities.Host()
        self.host_args.create_missing()
        # using CLI to create host
        self.host = Host.create({
            u'architecture-id': self.host_args.architecture.id,
            u'domain-id': self.host_args.domain.id,
            u'environment-id': self.host_args.environment.id,
            # pylint:disable=no-member
            u'location-id': self.host_args.location.id,
            u'mac': self.host_args.mac,
            u'medium-id': self.host_args.medium.id,
            u'name': self.host_args.name,
            u'operatingsystem-id': self.host_args.operatingsystem.id,
            # pylint:disable=no-member
            u'organization-id': self.host_args.organization.id,
            u'partition-table-id': self.host_args.ptable.id,
            u'puppet-proxy-id': self.puppet_proxy['id'],
            u'root-pass': self.host_args.root_pass,
        })

    @tier1
    def test_positive_update_name_by_id(self):
        """A host can be updated with a new random name. Use id to
        access the host

        @feature: Hosts

        @assert: A host is updated and the name matches
        """
        for new_name in valid_hosts_list():
            with self.subTest(new_name):
                Host.update({
                    'id': self.host['id'],
                    'new-name': new_name,
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertEqual(
                    u'{0}.{1}'.format(
                        new_name,
                        self.host['domain'],
                    ).lower(),
                    self.host['name'],
                )

    @tier1
    def test_positive_update_name_by_name(self):
        """A host can be updated with a new random name. Use name to
        access the host

        @feature: Hosts

        @assert: A host is updated and the name matches
        """
        for new_name in valid_hosts_list():
            with self.subTest(new_name):
                Host.update({
                    'name': self.host['name'],
                    'new-name': new_name,
                })
                self.host = Host.info({
                    'name': u'{0}.{1}'
                            .format(new_name, self.host['domain']).lower()
                })
                self.assertEqual(
                    u'{0}.{1}'.format(
                        new_name,
                        self.host['domain'],
                    ).lower(),
                    self.host['name'],
                )

    @tier1
    def test_positive_update_mac_by_id(self):
        """A host can be updated with a new random MAC address. Use id
        to access the host

        @feature: Hosts

        @assert: A host is updated and the MAC address matches
        """
        new_mac = gen_mac()
        Host.update({
            'id': self.host['id'],
            'mac': new_mac,
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertEqual(self.host['mac'], new_mac)

    @tier1
    def test_positive_update_mac_by_name(self):
        """A host can be updated with a new random MAC address. Use name
        to access the host

        @feature: Hosts

        @assert: A host is updated and the MAC address matches
        """
        new_mac = gen_mac()
        Host.update({
            'mac': new_mac,
            'name': self.host['name'],
        })
        self.host = Host.info({'name': self.host['name']})
        self.assertEqual(self.host['mac'], new_mac)

    @tier2
    def test_positive_update_domain_by_id(self):
        """A host can be updated with a new domain. Use entities ids for
        association

        @feature: Hosts

        @assert: A host is updated and the domain matches
        """
        new_domain = make_domain({
            'location-id': self.host_args.location.id,
            'organization-id': self.host_args.organization.id,
        })
        Host.update({
            'domain-id': new_domain['id'],
            'id': self.host['id'],
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertEqual(self.host['domain'], new_domain['name'])

    @tier2
    def test_positive_update_domain_by_name(self):
        """A host can be updated with a new domain. Use entities names
        for association

        @feature: Hosts

        @assert: A host is updated and the domain matches
        """
        new_domain = make_domain({
            'location': self.host_args.location.name,
            'organization': self.host_args.organization.name,
        })
        Host.update({
            'domain': new_domain['name'],
            'name': self.host['name'],
        })
        self.host = Host.info({
            'name': '{0}.{1}'.format(
                self.host['name'].split('.')[0],
                new_domain['name'],
            )
        })
        self.assertEqual(self.host['domain'], new_domain['name'])

    @tier2
    def test_positive_update_env_by_id(self):
        """A host can be updated with a new environment. Use entities
        ids for association

        @feature: Hosts

        @assert: A host is updated and the environment matches
        """
        new_env = make_environment({
            'location-id': self.host_args.location.id,
            'organization-id': self.host_args.organization.id,
        })
        Host.update({
            'environment-id': new_env['id'],
            'id': self.host['id'],
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertEqual(self.host['environment'], new_env['name'])

    @tier2
    def test_positive_update_env_by_name(self):
        """A host can be updated with a new environment. Use entities
        names for association

        @feature: Hosts

        @assert: A host is updated and the environment matches
        """
        new_env = make_environment({
            'location': self.host_args.location.name,
            'organization': self.host_args.organization.name,
        })
        Host.update({
            'environment': new_env['name'],
            'name': self.host['name'],
        })
        self.host = Host.info({'name': self.host['name']})
        self.assertEqual(self.host['environment'], new_env['name'])

    @tier2
    def test_positive_update_arch_by_id(self):
        """A host can be updated with a new architecture. Use entities
        ids for association

        @feature: Hosts

        @assert: A host is updated and the architecture matches
        """
        new_arch = make_architecture({
            'location-id': self.host_args.location.id,
            'organization-id': self.host_args.organization.id,
        })
        OperatingSys.add_architecture({
            'architecture-id': new_arch['id'],
            'id': self.host_args.operatingsystem.id,
        })
        Host.update({
            'architecture-id': new_arch['id'],
            'id': self.host['id'],
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertEqual(self.host['architecture'], new_arch['name'])

    @tier2
    def test_positive_update_arch_by_name(self):
        """A host can be updated with a new architecture. Use entities
        names for association

        @feature: Hosts

        @assert: A host is updated and the architecture matches
        """
        new_arch = make_architecture({
            'location': self.host_args.location.name,
            'organization': self.host_args.organization.name,
        })
        OperatingSys.add_architecture({
            'architecture': new_arch['name'],
            'title': self.host_args.operatingsystem.title,
        })
        Host.update({
            'architecture': new_arch['name'],
            'name': self.host['name'],
        })
        self.host = Host.info({'name': self.host['name']})
        self.assertEqual(self.host['architecture'], new_arch['name'])

    @tier2
    def test_positive_update_os_by_id(self):
        """A host can be updated with a new operating system. Use
        entities ids for association

        @feature: Hosts

        @assert: A host is updated and the operating system matches
        """
        new_os = make_os({
            'architecture-ids': self.host_args.architecture.id,
            'partition-table-ids': self.host_args.ptable.id,
        })
        Medium.add_operating_system({
            'id': self.host_args.medium.id,
            'operatingsystem-id': new_os['id'],
        })
        Host.update({
            'id': self.host['id'],
            'operatingsystem-id': new_os['id'],
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertEqual(self.host['operating-system'], new_os['title'])

    @tier2
    def test_positive_update_os_by_name(self):
        """A host can be updated with a new operating system. Use
        entities names for association

        @feature: Hosts

        @assert: A host is updated and the operating system matches
        """
        new_os = make_os({
            'architectures': self.host_args.architecture.name,
            'partition-tables': self.host['partition-table'],
        })
        Medium.add_operating_system({
            'name': self.host_args.medium.name,
            'operatingsystem': new_os['title'],
        })
        Host.update({
            'name': self.host['name'],
            'operatingsystem': new_os['title'],
        })
        self.host = Host.info({'name': self.host['name']})
        self.assertEqual(self.host['operating-system'], new_os['title'])

    @tier2
    def test_positive_update_medium_by_id(self):
        """A host can be updated with a new medium. Use entities ids for
        association

        @feature: Hosts

        @assert: A host is updated and the medium matches
        """
        new_medium = make_medium({
            'location-id': self.host_args.location.id,
            'organization-id': self.host_args.organization.id,
        })
        Medium.add_operating_system({
            'id': new_medium['id'],
            'operatingsystem-id': self.host_args.operatingsystem.id,
        })
        new_medium = Medium.info({'id': new_medium['id']})
        Host.update({
            'id': self.host['id'],
            'medium-id': new_medium['id'],
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertEqual(self.host['medium'], new_medium['name'])

    @tier2
    def test_positive_update_medium_by_name(self):
        """A host can be updated with a new medium. Use entities names
        for association

        @feature: Hosts

        @assert: A host is updated and the medium matches
        """
        new_medium = make_medium({
            'location': self.host_args.location.name,
            'organization': self.host_args.organization.name,
        })
        Medium.add_operating_system({
            'name': new_medium['name'],
            'operatingsystem': self.host_args.operatingsystem.title,
        })
        new_medium = Medium.info({'name': new_medium['name']})
        Host.update({
            'medium': new_medium['name'],
            'name': self.host['name'],
        })
        self.host = Host.info({'name': self.host['name']})
        self.assertEqual(self.host['medium'], new_medium['name'])

    @tier1
    def test_negative_update_name(self):
        """A host can not be updated with invalid or empty name

        @feature: Hosts

        @assert: A host is not updated
        """
        for new_name in invalid_values_list():
            with self.subTest(new_name):
                with self.assertRaises(CLIReturnCodeError):
                    Host.update({
                        'id': self.host['id'],
                        'new-name': new_name,
                    })
                self.host = Host.info({'id': self.host['id']})
                self.assertNotEqual(
                    u'{0}.{1}'.format(
                        new_name,
                        self.host['domain'],
                    ).lower(),
                    self.host['name'],
                )

    @tier1
    def test_negative_update_mac(self):
        """A host can not be updated with invalid or empty MAC address

        @feature: Hosts

        @assert: A host is not updated
        """
        for new_mac in invalid_values_list():
            with self.subTest(new_mac):
                with self.assertRaises(CLIReturnCodeError):
                    Host.update({
                        'id': self.host['id'],
                        'mac': new_mac,
                    })
                    self.host = Host.info({'id': self.host['id']})
                    self.assertEqual(self.host['mac'], new_mac)

    @tier2
    def test_negative_update_arch(self):
        """A host can not be updated with a architecture, which does not
        belong to host's operating system

        @feature: Hosts

        @assert: A host is not updated
        """
        new_arch = make_architecture({
            'location': self.host_args.location.name,
            'organization': self.host_args.organization.name,
        })
        with self.assertRaises(CLIReturnCodeError):
            Host.update({
                'architecture': new_arch['name'],
                'id': self.host['id'],
            })
        self.host = Host.info({'id': self.host['id']})
        self.assertNotEqual(self.host['architecture'], new_arch['name'])

    @tier2
    def test_negative_update_os(self):
        """A host can not be updated with a operating system, which is
        not associated with host's medium

        @feature: Hosts

        @assert: A host is not updated
        """
        new_arch = make_architecture({
            'location': self.host_args.location.name,
            'organization': self.host_args.organization.name,
        })
        new_os = make_os({
            'architectures': new_arch['name'],
            'partition-tables': self.host['partition-table'],
        })
        with self.assertRaises(CLIReturnCodeError):
            Host.update({
                'architecture': new_arch['name'],
                'id': self.host['id'],
                'operatingsystem': new_os['title'],
            })
        self.host = Host.info({'id': self.host['id']})
        self.assertNotEqual(self.host['operating-system'], new_os['title'])


class HostParameterTestCase(CLITestCase):
    """Tests targeting host parameters"""

    @classmethod
    def setUpClass(cls):
        """Create host to tests parameters for"""
        super(HostParameterTestCase, cls).setUpClass()
        cls.proxies = Proxy.list()
        assert len(cls.proxies) > 0
        cls.puppet_proxy = cls.proxies[0]
        # using nailgun to create dependencies
        cls.host = entities.Host()
        cls.host.create_missing()
        # using CLI to create host
        cls.host = Host.create({
            u'architecture-id': cls.host.architecture.id,
            u'domain-id': cls.host.domain.id,
            u'environment-id': cls.host.environment.id,
            u'location-id': cls.host.location.id,  # pylint:disable=no-member
            u'mac': cls.host.mac,
            u'medium-id': cls.host.medium.id,
            u'name': cls.host.name,
            u'operatingsystem-id': cls.host.operatingsystem.id,
            # pylint:disable=no-member
            u'organization-id': cls.host.organization.id,
            u'partition-table-id': cls.host.ptable.id,
            u'puppet-proxy-id': cls.puppet_proxy['id'],
            u'root-pass': cls.host.root_pass,
        })

    @tier1
    def test_positive_add_parameter_with_name(self):
        """Add host parameter with different valid names.

        @Feature: Hosts

        @Assert: Host parameter was successfully added with correct name.

        """
        for name in valid_data_list():
            with self.subTest(name):
                name = name.lower()
                Host.set_parameter({
                    'host-id': self.host['id'],
                    'name': name,
                    'value': gen_string('alphanumeric'),
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertIn(name, self.host['parameters'].keys())

    @tier1
    def test_positive_add_parameter_with_value(self):
        """Add host parameter with different valid values.

        @Feature: Hosts

        @Assert: Host parameter was successfully added with value.

        """
        for value in valid_data_list():
            with self.subTest(value):
                name = gen_string('alphanumeric').lower()
                Host.set_parameter({
                    'host-id': self.host['id'],
                    'name': name,
                    'value': value,
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertIn(name, self.host['parameters'].keys())
                self.assertEqual(value, self.host['parameters'][name])

    @tier1
    def test_positive_add_parameter_by_host_name(self):
        """Add host parameter by specifying host name.

        @Feature: Hosts

        @Assert: Host parameter was successfully added with correct name and
        value.

        """
        name = gen_string('alphanumeric').lower()
        value = gen_string('alphanumeric')
        Host.set_parameter({
            'host': self.host['name'],
            'name': name,
            'value': value,
        })
        self.host = Host.info({'id': self.host['id']})
        self.assertIn(name, self.host['parameters'].keys())
        self.assertEqual(value, self.host['parameters'][name])

    @tier1
    def test_positive_update_parameter_by_host_id(self):
        """Update existing host parameter by specifying host ID.

        @Feature: Hosts

        @Assert: Host parameter was successfully updated with new value.

        """
        name = gen_string('alphanumeric').lower()
        old_value = gen_string('alphanumeric')
        Host.set_parameter({
            'host-id': self.host['id'],
            'name': name,
            'value': old_value,
        })
        for new_value in valid_data_list():
            with self.subTest(new_value):
                Host.set_parameter({
                    'host-id': self.host['id'],
                    'name': name,
                    'value': new_value,
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertIn(name, self.host['parameters'].keys())
                self.assertEqual(new_value, self.host['parameters'][name])

    @tier1
    def test_positive_update_parameter_by_host_name(self):
        """Update existing host parameter by specifying host name.

        @Feature: Hosts

        @Assert: Host parameter was successfully updated with new value.

        """
        name = gen_string('alphanumeric').lower()
        old_value = gen_string('alphanumeric')
        Host.set_parameter({
            'host': self.host['name'],
            'name': name,
            'value': old_value,
        })
        for new_value in valid_data_list():
            with self.subTest(new_value):
                Host.set_parameter({
                    'host': self.host['name'],
                    'name': name,
                    'value': new_value,
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertIn(name, self.host['parameters'].keys())
                self.assertEqual(new_value, self.host['parameters'][name])

    @tier1
    def test_positive_delete_parameter_by_host_id(self):
        """Delete existing host parameter by specifying host ID.

        @Feature: Hosts

        @Assert: Host parameter was successfully deleted.

        """
        for name in valid_data_list():
            with self.subTest(name):
                name = name.lower()
                Host.set_parameter({
                    'host-id': self.host['id'],
                    'name': name,
                    'value': gen_string('alphanumeric'),
                })
                Host.delete_parameter({
                    'host-id': self.host['id'],
                    'name': name,
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertNotIn(name, self.host['parameters'].keys())

    @tier1
    def test_posistive_delete_parameter_by_host_name(self):
        """Delete existing host parameter by specifying host name.

        @Feature: Hosts

        @Assert: Host parameter was successfully deleted.

        """
        for name in valid_data_list():
            with self.subTest(name):
                name = name.lower()
                Host.set_parameter({
                    'host': self.host['name'],
                    'name': name,
                    'value': gen_string('alphanumeric'),
                })
                Host.delete_parameter({
                    'host': self.host['name'],
                    'name': name,
                })
                self.host = Host.info({'id': self.host['id']})
                self.assertNotIn(name, self.host['parameters'].keys())

    @tier1
    def test_negative_add_parameter(self):
        """Try to add host parameter with different invalid names.

        @Feature: Hosts

        @Assert: Host parameter was not added.

        """
        for name in invalid_values_list():
            with self.subTest(name):
                name = name.lower()
                with self.assertRaises(CLIReturnCodeError):
                    Host.set_parameter({
                        'host-id': self.host['id'],
                        'name': name,
                        'value': gen_string('alphanumeric'),
                    })
                self.host = Host.info({'id': self.host['id']})
                self.assertNotIn(name, self.host['parameters'].keys())


class KatelloAgentTestCase(CLITestCase):
    """Host tests, which require VM with installed katello-agent."""

    org = None
    env = None
    content_view = None
    activation_key = None

    @classmethod
    @skip_if_not_set('clients', 'fake_manifest')
    def setUpClass(cls):
        """Create Org, Lifecycle Environment, Content View, Activation key

        """
        super(KatelloAgentTestCase, cls).setUpClass()
        # Create new org, environment, CV and activation key
        KatelloAgentTestCase.org = make_org()
        KatelloAgentTestCase.env = make_lifecycle_environment({
            u'organization-id': KatelloAgentTestCase.org['id'],
        })
        KatelloAgentTestCase.content_view = make_content_view({
            u'organization-id': KatelloAgentTestCase.org['id'],
        })
        KatelloAgentTestCase.activation_key = make_activation_key({
            u'lifecycle-environment-id': KatelloAgentTestCase.env['id'],
            u'organization-id': KatelloAgentTestCase.org['id'],
        })
        # Add subscription to Satellite Tools repo to activation key
        setup_org_for_a_rh_repo({
            u'product': PRDS['rhel'],
            u'repository-set': REPOSET['rhst7'],
            u'repository': REPOS['rhst7']['name'],
            u'organization-id': KatelloAgentTestCase.org['id'],
            u'content-view-id': KatelloAgentTestCase.content_view['id'],
            u'lifecycle-environment-id': KatelloAgentTestCase.env['id'],
            u'activationkey-id': KatelloAgentTestCase.activation_key['id'],
        })
        # Create custom repo, add subscription to activation key
        setup_org_for_a_custom_repo({
            u'url': FAKE_0_YUM_REPO,
            u'organization-id': KatelloAgentTestCase.org['id'],
            u'content-view-id': KatelloAgentTestCase.content_view['id'],
            u'lifecycle-environment-id': KatelloAgentTestCase.env['id'],
            u'activationkey-id': KatelloAgentTestCase.activation_key['id'],
        })

    def setUp(self):
        """Create VM, subscribe it to satellite-tools repo, install katello-ca
        and katello-agent packages

        """
        super(KatelloAgentTestCase, self).setUp()
        # Create VM and register content host
        self.client = VirtualMachine(distro='rhel71')
        self.client.create()
        self.client.install_katello_ca()
        # Register content host, install katello-agent
        self.client.register_contenthost(
            KatelloAgentTestCase.activation_key['name'],
            KatelloAgentTestCase.org['label']
        )
        self.host = Host.info({'name': self.client.hostname})
        self.client.enable_repo(REPOS['rhst7']['id'])
        self.client.install_katello_agent()

    def tearDown(self):
        self.client.destroy()
        super(KatelloAgentTestCase, self).tearDown()

    @tier3
    @run_only_on('sat')
    def test_positive_get_errata_info(self):
        """Get errata info

        @Feature: Host - Errata

        @Assert: Errata info was displayed

        """
        self.client.download_install_rpm(
            FAKE_0_YUM_REPO,
            FAKE_0_CUSTOM_PACKAGE
        )
        result = Host.errata_info({
            u'host-id': self.host['id'],
            u'id': FAKE_0_ERRATA_ID,
        })
        self.assertEqual(result[0]['errata-id'], FAKE_0_ERRATA_ID)
        self.assertEqual(result[0]['packages'], FAKE_0_CUSTOM_PACKAGE)

    @tier3
    @run_only_on('sat')
    def test_positive_apply_errata(self):
        """Apply errata to a host

        @Feature: Host - Errata

        @Assert: Errata is scheduled for installation

        """
        self.client.download_install_rpm(
            FAKE_0_YUM_REPO,
            FAKE_0_CUSTOM_PACKAGE
        )
        Host.errata_apply({
            u'errata-ids': FAKE_0_ERRATA_ID,
            u'host-id': self.host['id'],
        })

    @tier3
    @run_only_on('sat')
    def test_positive_install_package(self):
        """Install a package to a host remotely

        @Feature: Host - Package

        @Assert: Package was successfully installed

        """
        Host.package_install({
            u'host-id': self.host['id'],
            u'packages': FAKE_0_CUSTOM_PACKAGE_NAME,
        })
        result = self.client.run(
            'rpm -q {0}'.format(FAKE_0_CUSTOM_PACKAGE_NAME)
        )
        self.assertEqual(result.return_code, 0)

    @tier3
    @run_only_on('sat')
    def test_positive_remove_package(self):
        """Remove a package from a host remotely

        @Feature: Host - Package

        @Assert: Package was successfully removed

        """
        self.client.download_install_rpm(
            FAKE_0_YUM_REPO,
            FAKE_0_CUSTOM_PACKAGE
        )
        Host.package_remove({
            u'host-id': self.host['id'],
            u'packages': FAKE_0_CUSTOM_PACKAGE_NAME,
        })
        result = self.client.run(
            'rpm -q {0}'.format(FAKE_0_CUSTOM_PACKAGE_NAME)
        )
        self.assertNotEqual(result.return_code, 0)

    @tier3
    @run_only_on('sat')
    def test_positive_upgrade_package(self):
        """Upgrade a host package remotely

        @Feature: Host - Package

        @Assert: Package was successfully upgraded

        """
        self.client.run('yum install -y {0}'.format(FAKE_1_CUSTOM_PACKAGE))
        Host.package_upgrade({
            u'host-id': self.host['id'],
            u'packages': FAKE_1_CUSTOM_PACKAGE_NAME,
        })
        result = self.client.run('rpm -q {0}'.format(FAKE_2_CUSTOM_PACKAGE))
        self.assertEqual(result.return_code, 0)

    @tier3
    @run_only_on('sat')
    def test_positive_upgrade_packages_all(self):
        """Upgrade all the host packages remotely

        @Feature: Host - Package

        @Assert: Packages (at least 1 with newer version available) were
        successfully upgraded

        """
        self.client.run('yum install -y {0}'.format(FAKE_1_CUSTOM_PACKAGE))
        Host.package_upgrade_all({'host-id': self.host['id']})
        result = self.client.run('rpm -q {0}'.format(FAKE_2_CUSTOM_PACKAGE))
        self.assertEqual(result.return_code, 0)

    @tier3
    @run_only_on('sat')
    def test_positive_install_package_group(self):
        """Install a package group to a host remotely

        @Feature: Host - Package group

        @Assert: Package group was successfully installed

        """
        Host.package_group_install({
            u'groups': FAKE_0_CUSTOM_PACKAGE_GROUP_NAME,
            u'host-id': self.host['id'],
        })
        for package in FAKE_0_CUSTOM_PACKAGE_GROUP:
            result = self.client.run('rpm -q {0}'.format(package))
            self.assertEqual(result.return_code, 0)

    @tier3
    @run_only_on('sat')
    def test_positive_remove_package_group(self):
        """Remove a package group from a host remotely

        @Feature: Host - Package group

        @Assert: Package group was successfully removed

        """
        hammer_args = {
            u'groups': FAKE_0_CUSTOM_PACKAGE_GROUP_NAME,
            u'host-id': self.host['id'],
        }
        Host.package_group_install(hammer_args)
        Host.package_group_remove(hammer_args)
        for package in FAKE_0_CUSTOM_PACKAGE_GROUP:
            result = self.client.run('rpm -q {0}'.format(package))
            self.assertNotEqual(result.return_code, 0)

    @tier3
    def test_negative_unregister_and_pull_content(self):
        """Attempt to retrieve content after host has been unregistered from
        Satellite

        @feature: Host

        @assert: Host can no longer retrieve content from satellite
        """
        result = self.client.run('subscription-manager unregister')
        self.assertEqual(result.return_code, 0)
        result = self.client.run(
            'yum install -y {0}'.format(FAKE_1_CUSTOM_PACKAGE))
        self.assertNotEqual(result.return_code, 0)

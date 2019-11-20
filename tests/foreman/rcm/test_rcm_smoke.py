"""
Smoke test for RCM to run when testing new published errata on CDN.

"""
import yaml

from nailgun import entities
from robottelo import constants
from robottelo import cli
from robottelo import manifests

from robottelo.products import YumRepository
from robottelo.test import TestCase
from robottelo.api.utils import enable_rhrepo_and_fetchid


repo_lists = """
rcm_smoke_test:
    'rhel-7-server-dotnet-debug-rpms':
        packages: 3
        errata: 3
    rhel-7-server-ansible-2-rpms:
        packages: 10
        errata: 3
    rhel-8-for-x86_64-baseos-rpms:
        packages: 100
        errata: 3
"""
def load_repo_info() -> dict:
    # Load from variable for testing, will probably be a file later
    repos_info = yaml.load(repo_lists)['rcm_smoke_test']
    return repos_info

def find_repo_sets(org, repo_label):
    return entities.RepositorySet().search(
        query={'organization_id': str(org.id), 'search': 'label = {}'.format(repo_label)})


class RCMSmokeTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RCMSmokeTest, cls).setUpClass()
        cls.org = entities.Organization().create()
        cls.lce = entities.LifecycleEnvironment(organization=cls.org).create()
        manifests.upload_manifest_locked(cls.org)
        cls.repo_info = load_repo_info()
        cls.repo_labels = cls.repo_info.keys()

    def setUp(self) -> None:
        super().setUp()

    def test_rcm_smoke(self):

        # first we go through and enable the repos, and ensure there aren't duplicates
        repo_sets = []
        for repo_label in self.repo_labels:
            rs = find_repo_sets(self.org, repo_label)
            self.assertEqual(len(rs), 1, "Verify only 1 repo named {} exists".format(repo_label))
            rs[0].enable()
            repo_sets.append(rs[0])





class Debug(TestCase):

    @classmethod
    def setUpClass(cls):
        super(Debug, cls).setUpClass()
        cls.org = entities.Organization(id=1).read()
        cls.lce = entities.LifecycleEnvironment(organization=cls.org, id=1).read()


    def test_debug(self):
        repo_sets = []
        repo_label = 'rhel-7-server-dotnet-rpms'
        rs = find_repo_sets(self.org, repo_label)
        self.assertEqual(len(rs), 1, "Verify only 1 repo named {} exists".format(repo_label))
        rs[0].enable()
        repo_sets.append(rs[0])

        print(repo_sets)





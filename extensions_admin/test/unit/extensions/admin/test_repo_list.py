import unittest
# NEED TO VERIFY

from mock import Mock
from pulp.common import constants as pulp_constants

from pulp_openstack.common import constants
from pulp_openstack.extensions.admin.repo_list import ListOpenstackRepositoriesCommand


class TestListOpenstackRepositoriesCommand(unittest.TestCase):
    def setUp(self):
        self.context = Mock()
        self.context.config = {'output': {'poll_frequency_in_seconds': 3}}

    def test_get_all_repos(self):
        self.context.server.repo.repositories.return_value.response_body = 'foo'
        command = ListOpenstackRepositoriesCommand(self.context)
        result = command._all_repos({'bar': 'baz'})
        self.context.server.repo.repositories.assert_called_once_with({'bar': 'baz'})
        self.assertEquals('foo', result)

    def test_get_all_repos_caches_results(self):
        command = ListOpenstackRepositoriesCommand(self.context)
        command.all_repos_cache = 'foo'
        result = command._all_repos({'bar': 'baz'})
        self.assertFalse(self.context.server.repo.repositories.called)
        self.assertEquals('foo', result)

    def test_get_repositories(self):
        # Setup
        repos = [
            {
                'id': 'matching',
                'notes': {pulp_constants.REPO_NOTE_TYPE_KEY: constants.REPO_NOTE_GLANCE, },
                'importers': [
                    {'config': {}}
                ],
                'distributors': [
                    {'id': constants.CLI_WEB_DISTRIBUTOR_ID}
                ]
            },
            {'id': 'non-rpm-repo',
             'notes': {}}
        ]
        self.context.server.repo.repositories.return_value.response_body = repos

        # Test
        command = ListOpenstackRepositoriesCommand(self.context)
        repos = command.get_repositories({})

        # Verify
        self.assertEqual(1, len(repos))
        self.assertEqual(repos[0]['id'], 'matching')

    def test_get_repositories_no_details(self):
        # Setup
        repos = [
            {
                'id': 'foo',
                'display_name': 'bar',
                'notes': {pulp_constants.REPO_NOTE_TYPE_KEY: constants.REPO_NOTE_GLANCE, }
            }
        ]
        self.context.server.repo.repositories.return_value.response_body = repos

        # Test
        command = ListOpenstackRepositoriesCommand(self.context)
        repos = command.get_repositories({})

        # Verify
        self.assertEqual(1, len(repos))
        self.assertEqual(repos[0]['id'], 'foo')
        self.assertTrue('importers' not in repos[0])
        self.assertTrue('distributors' not in repos[0])

    def test_get_other_repositories(self):
        # Setup
        repos = [
            {
                'repo_id': 'matching',
                'notes': {pulp_constants.REPO_NOTE_TYPE_KEY: constants.REPO_NOTE_GLANCE, },
                'distributors': [
                    {'id': constants.CLI_EXPORT_DISTRIBUTOR_ID},
                    {'id': constants.CLI_WEB_DISTRIBUTOR_ID}
                ]
            },
            {
                'repo_id': 'non-rpm-repo-1',
                'notes': {}
            }
        ]
        self.context.server.repo.repositories.return_value.response_body = repos

        # Test
        command = ListOpenstackRepositoriesCommand(self.context)
        repos = command.get_other_repositories({})

        # Verify
        self.assertEqual(1, len(repos))
        self.assertEqual(repos[0]['repo_id'], 'non-rpm-repo-1')

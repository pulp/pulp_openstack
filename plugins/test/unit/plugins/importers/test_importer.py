import unittest
# NEED TO VERIFY

import mock
from pulp.plugins.config import PluginCallConfiguration
from pulp.plugins.model import Repository

import data
from pulp_openstack.common import constants
from pulp_openstack.plugins.importers.importer import OpenstackImageImporter


class TestBasics(unittest.TestCase):
    def test_metadata(self):
        metadata = OpenstackImageImporter.metadata()

        self.assertEqual(metadata['id'], constants.IMPORTER_TYPE_ID)
        self.assertEqual(metadata['types'], [constants.IMAGE_TYPE_ID])
        self.assertTrue(len(metadata['display_name']) > 0)


class TestImportUnits(unittest.TestCase):

    def setUp(self):
        self.unit_key = {'arch': data.cirros_img_metadata['arch']}
        self.source_repo = Repository('repo_source')
        self.dest_repo = Repository('repo_dest')
        self.conduit = mock.MagicMock()
        self.config = PluginCallConfiguration({}, {})

    def test_import_all(self):
        mock_unit = mock.Mock(unit_key={'image_checksum':
                                        '5a46e37274928bb39f84415e2ef61240'}, metadata={})
        self.conduit.get_source_units.return_value = [mock_unit]
        result = OpenstackImageImporter().import_units(self.source_repo, self.dest_repo,
                                                       self.conduit, self.config)
        self.assertEquals(result, [mock_unit])
        self.conduit.associate_unit.assert_called_once_with(mock_unit)

    def test_import(self):
        mock_unit = mock.Mock(unit_key={'image_checksum':
                                        '5a46e37274928bb39f84415e2ef61240'}, metadata={})
        result = OpenstackImageImporter().import_units(self.source_repo, self.dest_repo,
                                                       self.conduit, self.config, units=[mock_unit])
        self.assertEquals(result, [mock_unit])
        self.conduit.associate_unit.assert_called_once_with(mock_unit)


class TestValidateConfig(unittest.TestCase):
    def test_always_true(self):
        for repo, config in [['a', 'b'], [1, 2], [mock.Mock(), {}], ['abc', {'a': 2}]]:
            # make sure all attempts are validated
            self.assertEqual(OpenstackImageImporter().validate_config(repo, config), (True, ''))

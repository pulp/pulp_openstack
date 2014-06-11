import unittest
# NEED TO VERIFY

import mock

from pulp_openstack.common import constants
from pulp_openstack.extensions.admin.upload import UploadOpenstackImageCommand
import data


test_config = {
    'filesystem': {'upload_working_dir': '~/.pulp/upload/'},
    'output': {'poll_frequency_in_seconds': 2},
}


class TestDetermineID(unittest.TestCase):
    def setUp(self):
        self.context = mock.MagicMock()
        self.context.config = test_config
        self.command = UploadOpenstackImageCommand(self.context)

    def test_return_value(self):
        ret = self.command.determine_type_id('/a/b/c')

        self.assertEqual(ret, constants.IMAGE_TYPE_ID)


class TestGenerateUnitKeyAndMetadata(unittest.TestCase):
    def setUp(self):
        self.context = mock.MagicMock()
        self.context.config = test_config
        self.command = UploadOpenstackImageCommand(self.context)

    def test_with_cirros(self):
        unit_key, metadata = self.command.generate_unit_key_and_metadata(data.cirros_img_path)

        self.assertEqual(unit_key, {'image_checksum': '64d7c1cd2b6f60c92c14662941cb7913',
                                    'image_size': 13167616,
                                    'image_filename': 'cirros-0.3.2-x86_64-disk.img'})
        self.assertEqual(metadata, {})

    def test_file_does_not_exist(self):
        self.assertRaises(IOError, self.command.generate_unit_key_and_metadata, '/a/b/c/d')

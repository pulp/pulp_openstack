import unittest
from mock import Mock

from pulp_openstack.common import models


class TestBasics(unittest.TestCase):
    def test_init_info(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0',
                                      {'image_size': 10000,
                                       'image_filename': 'a_filename.img',
                                       'name': 'test image', 'min_ram': 1024})

        self.assertEqual(image.image_checksum, '70924d6fa4b2d745185fa4660703a5c0')

    def test_unit_key(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0',
                                      {'image_filename': 'a_filename.img',
                                       'name': 'test image', 'min_ram': 1024,
                                       'image_size': 10000})

        self.assertEqual(image.unit_key, {'image_checksum': '70924d6fa4b2d745185fa4660703a5c0'})

    def test_relative_path(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0',
                                      {'image_filename': 'a_filename.img',
                                       'name': 'test image', 'min_ram': 1024,
                                       'image_size': 10000})

        self.assertEqual(image.relative_path, '70924d6fa4b2d745185fa4660703a5c0')

    def test_metadata(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0',
                                      {'image_filename': 'a_filename.img',
                                       'name': 'test image', 'min_ram': 1024,
                                       'image_size': 10000})
        self.assertEqual(image.metadata, {'min_ram': 1024, 'name': 'test image',
                                          'image_filename': 'a_filename.img', 'image_size': 10000})

    def test_metadata_add_props(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0',
                                      {'image_filename': 'a_filename.img',
                                       'name': 'test image', 'min_ram': 1024,
                                       'image_size': 10000})
        self.assertEqual(image.metadata, {'name': 'test image', 'min_ram': 1024,
                                          'image_filename': 'a_filename.img', 'image_size': 10000})

    def test_init_unit(self):
        mock_conduit = Mock()
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0',
                                      {'name': 'test image', 'min_ram': 1024,
                                       'image_size': 10000,
                                       'image_filename': 'a_filename.img'})
        image.init_unit(mock_conduit)
        expected_call = ('openstack_image', {'image_checksum': '70924d6fa4b2d745185fa4660703a5c0'},
                         {'min_ram': 1024, 'image_filename': 'a_filename.img',
                          'name': 'test image', 'image_size': 10000},
                         '70924d6fa4b2d745185fa4660703a5c0/a_filename.img')
        mock_conduit.init_unit.assert_called_once_with(*expected_call)

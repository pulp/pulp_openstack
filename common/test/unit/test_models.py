import unittest

from pulp_openstack.common import models


class TestBasics(unittest.TestCase):
    def test_init_info(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0', 10000, 'a_filename.img')

        self.assertEqual(image.image_checksum, '70924d6fa4b2d745185fa4660703a5c0')
        self.assertEqual(image.image_size, 10000)

    def test_unit_key(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0', 10000, 'a_filename.img')

        self.assertEqual(image.unit_key, {'image_checksum': '70924d6fa4b2d745185fa4660703a5c0',
                                          'image_size': 10000, 'image_filename': 'a_filename.img'})

    def test_relative_path(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0', 10000, 'a_filename.img')

        self.assertEqual(image.relative_path, 'openstack_image/70924d6fa4b2d745185fa4660703a5c0')

    def test_metadata(self):
        image = models.OpenstackImage('70924d6fa4b2d745185fa4660703a5c0', 10000, 'a_filename.img')

        metadata = image.unit_metadata
        self.assertEqual(metadata, {})

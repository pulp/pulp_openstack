import shutil
import tempfile
import unittest

from mock import Mock, MagicMock, patch
from pulp.plugins.distributor import Distributor

from pulp_openstack.common import constants
from pulp_openstack.plugins.distributors.distributor_glance import OpenstackImageGlanceDistributor
from pulp_openstack.plugins.distributors.distributor_glance import entry_point


class TestEntryPoint(unittest.TestCase):
    def test_returns_importer(self):
        distributor, config = entry_point()

        self.assertTrue(issubclass(distributor, Distributor))

    def test_returns_config(self):
        distributor, config = entry_point()

        # make sure it's at least the correct type
        self.assertTrue(isinstance(config, dict))


class TestBasics(unittest.TestCase):

    def setUp(self):
        self.distributor = OpenstackImageGlanceDistributor()
        self.working_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.working_dir, ignore_errors=True)

    def test_metadata(self):
        metadata = OpenstackImageGlanceDistributor.metadata()

        self.assertEqual(metadata['id'], constants.DISTRIBUTOR_GLANCE_TYPE_ID)
        self.assertEqual(metadata['types'], [constants.IMAGE_TYPE_ID])
        self.assertTrue(len(metadata['display_name']) > 0)

    @patch('pulp_openstack.plugins.distributors.distributor_glance.configuration.validate_config')
    def test_validate_config(self, mock_validate):
        value = self.distributor.validate_config(Mock(), 'foo', Mock())
        mock_validate.assert_called_once_with('foo')
        self.assertEquals(value, mock_validate.return_value)

    @patch('pulp_openstack.plugins.distributors.distributor_glance.GlancePublisher')
    def test_publish_repo(self, mock_glance_publisher):
        (mock_repo, mock_conduit, mock_config) = (Mock(), Mock(), Mock())
        self.distributor.publish_repo(mock_repo, mock_conduit, mock_config)
        mock_glance_publisher.publish.assert_called_once()

    def test_cancel_publish_repo(self):
        self.distributor._publisher = MagicMock()
        self.distributor.cancel_publish_repo()
        self.assertTrue(self.distributor.canceled)
        self.distributor._publisher.cancel.assert_called_once()

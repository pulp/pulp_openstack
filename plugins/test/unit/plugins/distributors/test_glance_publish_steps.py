import os
import shutil
import tempfile
import unittest

from mock import Mock, patch, call, MagicMock

from pulp.devel.unit.util import touch

from pulp.plugins.conduits.repo_publish import RepoPublishConduit
from pulp.plugins.model import Repository
from pulp.plugins.util.publish_step import PublishStep

from pulp_openstack.plugins.distributors import glance_publish_steps


class TestPublishImagesStep(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.working_directory = os.path.join(self.temp_dir, 'working')
        self.content_directory = os.path.join(self.temp_dir, 'content')
        os.makedirs(self.working_directory)
        os.makedirs(self.content_directory)
        repo = Repository('foo_repo_id', working_dir=self.working_directory)
        config = Mock()
        config.get_config.return_value = "mocked-config-value"
        conduit = RepoPublishConduit(repo.id, 'foo_repo')
        self.parent = PublishStep('test-step', repo, conduit, config)

    def tearDown(self):
        shutil.rmtree(self.working_directory)

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_process_unit(self, mock_ou):
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        self.assertEquals(step.images_processed, [])
        step.parent = self.parent
        fake_image_filename = 'fake-zero-byte-image.qcow2'
        touch(os.path.join(self.content_directory, fake_image_filename))
        unit = Mock(unit_key={'image_checksum': 'd41d8cd98f00b204e9800998ecf8427e'},
                    metadata={'image_size': 100, 'image_name': 'fake-image-name'},
                    storage_path=os.path.join(self.content_directory, fake_image_filename))
        step.get_working_dir = Mock(return_value=self.working_directory)
        step.process_unit(unit)
        expected_calls = [call().find_image('foo_repo_id', 'd41d8cd98f00b204e9800998ecf8427e'),
                          call().create_image(os.path.join(self.content_directory,
                                                           fake_image_filename),
                                              'foo_repo_id',
                                              checksum='d41d8cd98f00b204e9800998ecf8427e',
                                              name='fake-image-name', size=100)]

        mock_ou.assert_has_calls(expected_calls, any_order=True)

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_process_unit_already_exists(self, mock_openstackutil):
        mock_ou = mock_openstackutil.return_value
        mock_ou.find_image.return_value = iter(['an-image'])
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        step.parent = self.parent
        fake_image_filename = 'fake-zero-byte-image.qcow2'
        touch(os.path.join(self.content_directory, fake_image_filename))
        unit = Mock(unit_key={'image_checksum': 'd41d8cd98f00b204e9800998ecf8427e'},
                    metadata={'image_size': 100, 'image_name': 'fake-image-name'},
                    storage_path=os.path.join(self.content_directory, fake_image_filename))
        step.get_working_dir = Mock(return_value=self.working_directory)

        step.process_unit(unit)
        unexpected_call = call().create_image(os.path.join(self.content_directory,
                                                           fake_image_filename),
                                              'foo_repo_id',
                                              checksum='d41d8cd98f00b204e9800998ecf8427e',
                                              name='fake-image-name', size=100)
        # make sure "create_image" was not called
        self.assertTrue(unexpected_call not in mock_ou.mock_calls)

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_process_unit_found_multiple_images(self, mock_openstackutil):
        mock_ou = mock_openstackutil.return_value
        mock_ou.find_image.return_value = iter(['an-image', 'image2'])
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        step.parent = self.parent
        fake_image_filename = 'fake-zero-byte-image.qcow2'
        touch(os.path.join(self.content_directory, fake_image_filename))
        unit = Mock(unit_key={'image_checksum': 'd41d8cd98f00b204e9800998ecf8427e'},
                    metadata={'image_size': 100, 'image_name': 'fake-image-name'},
                    storage_path=os.path.join(self.content_directory, fake_image_filename))
        step.get_working_dir = Mock(return_value=self.working_directory)

        try:
            step.process_unit(unit)
            self.assertTrue(False, "RuntimeError not thrown")
        except RuntimeError:
            pass

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_finalize_no_deletes(self, mock_ou):
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        self.assertEquals(step.images_processed, [])
        step.parent = self.parent
        step.finalize()
        expected_calls = [call().find_repo_images('foo_repo_id')]

        mock_ou.assert_has_calls(expected_calls, any_order=True)

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_finalize_with_deletes(self, mock_openstackutil):
        mock_ou = mock_openstackutil.return_value
        mock_image = MagicMock()
        mock_image.id = "mock_image_id"

        mock_ou.find_repo_images.return_value = iter([mock_image])
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        self.assertEquals(step.images_processed, [])
        step.parent = self.parent
        step.finalize()
        mock_ou.delete_image.assert_called_once()

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_finalize_no_deletes_with_images(self, mock_openstackutil):
        mock_ou = mock_openstackutil.return_value
        mock_image = MagicMock()
        mock_image.id = "mock_image_id"
        mock_image.checksum = "mock_image_checksum"

        mock_ou.find_repo_images.return_value = iter([mock_image])
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        self.assertEquals(step.images_processed, [])
        step.parent = self.parent
        step.images_processed = [mock_image.checksum]
        step.finalize()
        self.assertEquals(mock_ou.delete_image.called, 0)

    @patch('pulp_openstack.common.openstack_utils.OpenstackUtils')
    def test_finalize_bad_push(self, mock_openstackutil):
        """
        Tests that if an image didn't make it from pulp to glance for some
        reason, we do not perform any deletions at all for that repo.
        """
        mock_ou = mock_openstackutil.return_value
        mock_image = MagicMock()
        mock_image.id = "mock_image_id"
        mock_image.checksum = "mock_image_checksum"
        unpushed_mock_image = MagicMock()
        unpushed_mock_image.id = "unpushed_mock_image_id"
        unpushed_mock_image.checksum = "unpushed_mock_image_id_checksum"

        mock_ou.find_repo_images.return_value = iter([mock_image])
        mock_config = Mock()
        mock_config.get_config.return_value = "mocked-config-value"
        step = glance_publish_steps.PublishImagesStep()
        step.config = mock_config
        step.initialize()
        self.assertEquals(step.images_processed, [])
        step.parent = self.parent
        step.images_processed = [mock_image.checksum, unpushed_mock_image.checksum]
        try:
            step.finalize()
            self.assertTrue(False, "finalize should have thrown RuntimeError")
        except RuntimeError:
            self.assertEquals(mock_ou.delete_image.called, 0)


class TestGlancePublisher(unittest.TestCase):

    def setUp(self):
        self.working_directory = tempfile.mkdtemp()
        self.master_dir = os.path.join(self.working_directory, 'master')
        self.working_temp = os.path.join(self.working_directory, 'work')
        self.repo = Mock(id='foo', working_dir=self.working_temp)

    def tearDown(self):
        shutil.rmtree(self.working_directory)

    @patch('pulp_openstack.plugins.distributors.glance_publish_steps.PublishImagesStep')
    def test_init(self, mock_glance_publish_step):
        mock_conduit = Mock()
        mock_config = {}
        publisher = glance_publish_steps.GlancePublisher(self.repo, mock_conduit, mock_config)
        self.assertEquals(publisher.children, [mock_glance_publish_step.return_value])

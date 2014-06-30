import unittest

from mock import patch, MagicMock

from pulp_openstack.common.openstack_utils import OpenstackUtils


class TestOpenstackUtils(unittest.TestCase):

    @patch('keystoneclient.v2_0.client.Client')
    @patch('glanceclient.v2.client.Client')
    def test_init(self, mock_glclient, mock_ksclient):
        login_args = {'username': 'test-user',
                      'password': 'test-pw',
                      'tenant_name': 'test-tenant',
                      'auth_url': 'http://auth.url/blah'}

        OpenstackUtils(**login_args)
        mock_ksclient.assert_called_once_with(username='test-user', tenant_name='test-tenant',
                                              password='test-pw', auth_url='http://auth.url/blah')

    @patch('keystoneclient.v2_0.client.Client')
    @patch('glanceclient.v2.client.Client')
    def test_create(self, mock_glclient, mock_ksclient):
        mock_glclient().images.get().checksum = '1234abc'
        mock_glclient().images.get().size = 100

        login_args = {'username': 'test-user',
                      'password': 'test-pw',
                      'tenant_name': 'test-tenant',
                      'auth_url': 'http://auth.url/blah'}

        ou = OpenstackUtils(**login_args)
        image_filename = 'common/test/data/cirros-0.3.2-x86_64-disk.img'
        ou.create_image(image_filename, 'fake-repoid', name='some name',
                        checksum='1234abc', size=100)

        # test with bad checksum
        try:
            ou.create_image(image_filename, 'fake-repoid', name='some name',
                            checksum='1234abcdef', size=100)
            self.assertTrue(False, "should not get here, exception not thrown")
        except RuntimeError:
            pass

        # test with bad size
        try:
            ou.create_image(image_filename, 'fake-repoid', name='some name',
                            checksum='1234abc', size=999)
            self.assertTrue(False, "should not get here, exception not thrown")
        except RuntimeError:
            pass

    @patch('keystoneclient.v2_0.client.Client')
    @patch('glanceclient.v2.client.Client')
    def test_find(self, mock_glclient, mock_ksclient):
        login_args = {'username': 'test-user',
                      'password': 'test-pw',
                      'tenant_name': 'test-tenant',
                      'auth_url': 'http://auth.url/blah'}

        ou = OpenstackUtils(**login_args)
        ou.find_image('some-repo-id', '1234abc')
        mock_glclient().images.list.assert_called_with(filters={'checksum': '1234abc',
                                                                'pulp_repo_id': 'some-repo-id',
                                                                'from_pulp': 'true'})

    @patch('keystoneclient.v2_0.client.Client')
    @patch('glanceclient.v2.client.Client')
    def test_delete(self, mock_glclient, mock_ksclient):
        login_args = {'username': 'test-user',
                      'password': 'test-pw',
                      'tenant_name': 'test-tenant',
                      'auth_url': 'http://auth.url/blah'}

        ou = OpenstackUtils(**login_args)
        mock_image = MagicMock()
        mock_image.id = 'image-id'
        ou.delete_image(mock_image)
        mock_glclient().images.delete.assert_called_with('image-id')

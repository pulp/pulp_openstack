import logging

import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient


_logger = logging.getLogger(__name__)


class OpenstackUtils():
    """
    Utilities for interacting with OpenStack

    Currently this is just for keystone and glance
    """

    def __init__(self, username=None, password=None, tenant_name=None, auth_url=None):
        """
        Initialize openstack util

        :param username: keystone username
        :type  username: string
        :param password: keystone password
        :type  password: string
        :param tenant_name: keystone tenant name
        :type  tenant_name: string
        :param auth_url: keystone authentication URL
        :type  auth_url: string
        """

        keystone_auth_args = {'username': username,
                              'password': password,
                              'tenant_name': tenant_name,
                              'auth_url': auth_url}
        _logger.info("obtaining keystone token for user %s, tenant %s against auth url %s" %
                     (username, tenant_name, auth_url))
        keystone_client = ksclient.Client(**keystone_auth_args)
        glance_endpoint = keystone_client.service_catalog.url_for(service_type='image',
                                                                  endpoint_type='publicURL')
        _logger.info("image endpoint from service catalog is %s" % glance_endpoint)
        self.glance_client = glclient.Client(glance_endpoint, token=keystone_client.auth_token)

    def create_image(self, filename, repo_id, name=None, checksum=None, size=None):
        """
        upload an image into glance

        :param filename: image filename
        :type  filename: string
        :param repo_id: id for pulp repo that the image is associated with
        :type  repo_id: string
        :param name: human-readable name for image
        :type  name: string
        :param checksum: checksum we expect image to have. This gets validated after the upload.
        :type  checksum: string
        :param size: size we expect image to have. This gets validated as after the upload.
        :type  size: int
        """
        # see http://docs.openstack.org/image-guide/content/image-formats.html
        # TODO; set private properties per flaper87
        image_args = {'name': name,
                      'container_format': 'bare',
                      'disk_format': 'qcow2',
                      'protected': True,
                      'visibility': 'public',  # this needs to be configurable!
                      'from_pulp': 'true',
                      'pulp_repo_id': repo_id}

        image = self.glance_client.images.create(**image_args)

        with open(filename, 'rb') as image_file:
            self.glance_client.images.upload(image.id, image_file)

        # grab the image metadata, verify checksum
        image = self.glance_client.images.get(image.id)
        if checksum != image.checksum:
            raise RuntimeError("checksum error! Expected %s, but got %s from server" %
                               (checksum, image.checksum))
        if size != image.size:
            raise RuntimeError("size error! Expected file size %s, but got %s from server" %
                               (size, image.size))

    def find_image(self, repo_id, image_checksum):
        """
        Find an image from openstack. If this returns more than one image, something bad happened.

        :param repo_id: repo name
        :type  repo_id: string
        :param image_checksum: image checksum
        :type  image_checksum: string
        :return: list of images as json dicts
        :rtype: iterator
        """
        filters = {'from_pulp': 'true',
                   'pulp_repo_id': repo_id,
                   'checksum': image_checksum}
        return self.glance_client.images.list(filters=filters)

    def find_repo_images(self, repo_id):
        """
        Find all images associated with a particular repo. This is useful to
        calculate which images need to be deleted (i.e., exists in glance but
        not pulp, yet are associated with a pulp repo).

        :param repo_id: repo name
        :type  repo_id: string
        :return: iterator of found images as json dicts
        :rtype: iterator
        """
        filters = {'from_pulp': 'true',
                   'pulp_repo_id': repo_id}
        return self.glance_client.images.list(filters=filters)

    def delete_image(self, image):
        """
        delete an image based on its ID

        :param image: image
        :type  image: image json
        """
        self.glance_client.images.update(image.id, protected=False)
        self.glance_client.images.delete(image.id)

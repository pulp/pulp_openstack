from gettext import gettext as _

import logging

from pulp.plugins.util.publish_step import PublishStep, UnitPublishStep

from pulp_openstack.common import constants
from pulp_openstack.common import openstack_utils

_logger = logging.getLogger(__name__)


class GlancePublisher(PublishStep):
    """
    Openstack Image Web publisher class that pushes images into Glance.
    """

    def __init__(self, repo, publish_conduit, config):
        """
        :param repo: Pulp managed Yum repository
        :type  repo: pulp.plugins.model.Repository
        :param publish_conduit: Conduit providing access to relative Pulp functionality
        :type  publish_conduit: pulp.plugins.conduits.repo_publish.RepoPublishConduit
        :param config: Pulp configuration for the distributor
        :type  config: pulp.plugins.config.PluginCallConfiguration
        """
        super(GlancePublisher, self).__init__(constants.PUBLISH_STEP_GLANCE_PUBLISHER,
                                              repo, publish_conduit, config)

        publish_step = PublishStep(constants.PUBLISH_STEP_OVER_GLANCE_REST)
        publish_step.description = _('Pushing files to Glance.')
        self.add_child(PublishImagesStep())


class PublishImagesStep(UnitPublishStep):
    """
    Publish Images
    """

    def __init__(self):
        """
        Initialize publisher.
        """
        super(PublishImagesStep, self).__init__(constants.PUBLISH_STEP_IMAGES,
                                                constants.IMAGE_TYPE_ID)
        self.context = None
        self.description = _('Publishing Image Files.')

    def initialize(self):
        """
        Initialize publisher (second phase).
        """
        _logger.info("initizialing, setting up connection to OpenStack")
        keystone_conf = {'username': self.get_config().get('keystone-username'),
                         'password': self.get_config().get('keystone-password'),
                         'tenant_name': self.get_config().get('keystone-tenant'),
                         'auth_url': self.get_config().get('keystone-url')}
        self.ou = openstack_utils.OpenstackUtils(**keystone_conf)

        # this is to keep track of images we touched during process_unit(). At
        # the end, anything untouched in glance that has the correct repo
        # metadata is deleted.
        self.images_processed = []

    def process_unit(self, unit):
        """
        Link the unit to the image content directory

        :param unit: The unit to process
        :type  unit: pulp_openstack.common.models.OpenstackImage
        """
        # we need to add the image checksum to our processed list ASAP, otherwise they will
        # be deleted via finalize()
        self.images_processed.append(unit.unit_key['image_checksum'])

        _logger.debug("pushing unit %s from repo %s to glance" % (unit, self.get_repo().id))
        images = list(self.ou.find_image(self.get_repo().id, unit.unit_key['image_checksum']))

        _logger.debug("found existing image in glance: %s" % images)
        if len(images) > 1:
            raise RuntimeError("more than one image found with same checksum for repo %s!" %
                               self.get_repo().id)

        if not images:
            self.ou.create_image(unit.storage_path, self.get_repo().id,
                                 name=unit.metadata['image_name'],
                                 checksum=unit.unit_key['image_checksum'],
                                 size=unit.metadata['image_size'])
        else:
            _logger.debug("image already exists, skipping publish")

    def finalize(self):
        """
        Finalize publish.

        This examines self.images_processed and performs any deletions.
        """
        # this could be more elegant
        glance_image_by_checksum = {}
        glance_images = self.ou.find_repo_images(self.get_repo().id)
        for glance_image in glance_images:
            glance_image_by_checksum[glance_image.checksum] = glance_image
        _logger.debug("images in glance associated with repo: %s" % glance_image_by_checksum.keys())

        pulp_image_checksums = self.images_processed
        _logger.debug("images in pulp associated with repo: %s" % pulp_image_checksums)

        for pulp_image_checksum in pulp_image_checksums:
            if pulp_image_checksum not in glance_image_by_checksum.keys():
                raise RuntimeError("Images found in pulp repo that were not published to glance. "
                                   "Please consult error log for more details.")

        for glance_image_checksum in glance_image_by_checksum:
            if glance_image_checksum not in pulp_image_checksums:
                _logger.info("deleting image with checksum %s from glance" % glance_image_checksum)
                self.ou.delete_image(glance_image_by_checksum[glance_image_checksum])

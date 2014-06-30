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

        # check for images to delete here

    def process_unit(self, unit):
        """
        Link the unit to the image content directory

        :param unit: The unit to process
        :type  unit: pulp_openstack.common.models.OpenstackImage
        """
        _logger.info("pushing image %s from repo %s to glance" % (unit, self.get_repo().id))
        images = list(self.ou.find_image(self.get_repo().id, unit.unit_key['image_checksum']))
        _logger.info("found existing images: %s" % images)
        if not images:
            self.ou.create_image(unit.storage_path, self.get_repo().id,
                                 name=unit.metadata['image_name'],
                                 checksum=unit.unit_key['image_checksum'],
                                 size=unit.metadata['image_size'])
        else:
            _logger.info("image already exists!")

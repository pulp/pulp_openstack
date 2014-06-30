from gettext import gettext as _

import logging
import os

from pulp.plugins.util.publish_step import PublishStep, UnitPublishStep, \
    AtomicDirectoryPublishStep

from pulp_openstack.common import constants
from pulp_openstack.plugins.distributors import configuration

_logger = logging.getLogger(__name__)


class WebPublisher(PublishStep):
    """
    Openstack Image Web publisher class that is responsible for the actual publishing
    of a openstack image repository via a web server
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
        super(WebPublisher, self).__init__(constants.PUBLISH_STEP_WEB_PUBLISHER,
                                           repo, publish_conduit, config)

        publish_dir = configuration.get_web_publish_dir(repo, config)
        self.web_working_dir = os.path.join(self.get_working_dir(), 'web')
        master_publish_dir = configuration.get_master_publish_dir(repo, config)
        atomic_publish_step = AtomicDirectoryPublishStep(self.get_working_dir(),
                                                         [('web', publish_dir)],
                                                         master_publish_dir,
                                                         step_type=constants.PUBLISH_STEP_OVER_HTTP)
        atomic_publish_step.description = _('Making files available via web.')
        self.add_child(PublishImagesStep())
        self.add_child(atomic_publish_step)


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
        self.redirect_context = None
        self.description = _('Publishing Image Files.')

    def process_unit(self, unit):
        """
        Link the unit to the image content directory

        :param unit: The unit to process
        :type  unit: pulp_openstack.common.models.OpenstackImage
        """
        # note: we do not use the image checksum in the published directory path
        target_base = os.path.join(self.get_web_directory())
        _logger.info("linking %s to %s" % (unit.storage_path,
                                           os.path.join(target_base,
                                                        os.path.basename(unit.storage_path))))
        self._create_symlink(unit.storage_path,
                             os.path.join(target_base, os.path.basename(unit.storage_path)))

    def finalize(self):
        """
        Close & finalize each the metadata context
        """
        if self.redirect_context:
            self.redirect_context.finalize()

    def get_web_directory(self):
        """
        Get the directory where the files published to the web have been linked
        :return: path to web directory
        :rtype: string
        """
        return os.path.join(self.get_working_dir(), 'web')

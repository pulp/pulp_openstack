from gettext import gettext as _

import os

from pulp.plugins.util.publish_step import PublishStep, UnitPublishStep, \
    AtomicDirectoryPublishStep

from pulp_openstack.common import constants
from pulp_openstack.plugins.distributors import configuration


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

    def finalize(self):
        """
        Close & finalize each the metadata context
        """
        if self.redirect_context:
            self.redirect_context.finalize()

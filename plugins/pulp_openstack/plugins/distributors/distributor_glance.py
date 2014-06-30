from gettext import gettext as _

import copy
import logging

from pulp.common.config import read_json_config
from pulp.plugins.distributor import Distributor

from pulp_openstack.common import constants
from pulp_openstack.plugins.distributors.glance_publish_steps import GlancePublisher
from pulp_openstack.plugins.distributors import configuration


_logger = logging.getLogger(__name__)

PLUGIN_DEFAULT_CONFIG = {
    constants.CONFIG_KEY_GLANCE_PUBLISH_DIRECTORY: constants.CONFIG_VALUE_GLANCE_PUBLISH_DIRECTORY
}


def entry_point():
    """
    Entry point that pulp platform uses to load the distributor
    :return: distributor class and its config
    :rtype:  Distributor, dict
    """
    plugin_config = copy.deepcopy(PLUGIN_DEFAULT_CONFIG)
    edited_config = read_json_config(constants.DISTRIBUTOR_CONFIG_FILE_NAME)

    plugin_config.update(edited_config)
    return OpenstackImageGlanceDistributor, plugin_config


class OpenstackImageGlanceDistributor(Distributor):
    """
    A class for publishing repos to glance.

    This class is still a work in progress.
    """

    @classmethod
    def metadata(cls):
        """
        Used by Pulp to classify the capabilities of this distributor. The
        following keys must be present in the returned dictionary:

        * id - Programmatic way to refer to this distributor. Must be unique
          across all distributors. Only letters and underscores are valid.
        * display_name - User-friendly identification of the distributor.
        * types - List of all content type IDs that may be published using this
          distributor.

        :return:    keys and values listed above
        :rtype:     dict
        """
        return {
            'id': constants.DISTRIBUTOR_GLANCE_TYPE_ID,
            'display_name': _('Openstack Image Glance Distributor'),
            'types': [constants.IMAGE_TYPE_ID]
        }

    def __init__(self):
        """
        Initialize distributor.
        """
        super(OpenstackImageGlanceDistributor, self).__init__()
        self._publisher = None
        self.canceled = False

    def validate_config(self, repo, config, config_conduit):
        """
        Allows the distributor to check the contents of a potential configuration
        for the given repository. This call is made both for the addition of
        this distributor to a new repository as well as updating the configuration
        for this distributor on a previously configured repository. The implementation
        should use the given repository data to ensure that updating the
        configuration does not put the repository into an inconsistent state.

        The return is a tuple of the result of the validation (True for success,
        False for failure) and a message. The message may be None and is unused
        in the success case. For a failed validation, the message will be
        communicated to the caller so the plugin should take i18n into
        consideration when generating the message.

        The related_repos parameter contains a list of other repositories that
        have a configured distributor of this type. The distributor configurations
        is found in each repository in the "plugin_configs" field.

        :param repo: metadata describing the repository to which the
                     configuration applies
        :type  repo: pulp.plugins.model.Repository

        :param config: plugin configuration instance; the proposed repo
                       configuration is found within
        :type  config: pulp.plugins.config.PluginCallConfiguration

        :param config_conduit: Configuration Conduit;
        :type  config_conduit: pulp.plugins.conduits.repo_config.RepoConfigConduit

        :return: tuple of (bool, str) to describe the result
        :rtype:  tuple
        """
        return configuration.validate_config(config)

    def publish_repo(self, repo, publish_conduit, config):
        """
        Publishes the given repository.

        While this call may be implemented using multiple threads, its execution
        from the Pulp server's standpoint should be synchronous. This call should
        not return until the publish is complete.

        It is not expected that this call be atomic. Should an error occur, it
        is not the responsibility of the distributor to rollback any changes
        that have been made.

        :param repo: metadata describing the repository
        :type  repo: pulp.plugins.model.Repository

        :param publish_conduit: provides access to relevant Pulp functionality
        :type  publish_conduit: pulp.plugins.conduits.repo_publish.RepoPublishConduit

        :param config: plugin configuration
        :type  config: pulp.plugins.config.PluginConfiguration

        :return: report describing the publish run
        :rtype:  pulp.plugins.model.PublishReport
        """
        _logger.debug('Publishing openstack image repository: %s' % repo.id)
        self._publisher = GlancePublisher(repo, publish_conduit, config)
        return self._publisher.publish()

    def cancel_publish_repo(self):
        """
        Call cancellation control hook.
        """
        _logger.debug('Canceling openstack image repository publish')
        self.canceled = True
        if self._publisher is not None:
            self._publisher.cancel()

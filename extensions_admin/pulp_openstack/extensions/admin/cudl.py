from gettext import gettext as _

from pulp.client import parsers
from pulp.client.commands.repo.cudl import CreateAndConfigureRepositoryCommand
from pulp.common.constants import REPO_NOTE_TYPE_KEY
from pulp.client.extensions.extensions import PulpCliOption

from pulp_openstack.common import constants


d = _('if "true", on each successful sync the repository will automatically be '
      'published; if "false" content will only be available after manually publishing '
      'the repository; defaults to "true"')
OPT_AUTO_PUBLISH = PulpCliOption('--auto-publish', d, required=False,
                                 parse_func=parsers.parse_boolean)

d = _('if "true" requests for this repo will be checked for an entitlement certificate authorizing '
      'the server url for this repository; if "false" no authorization checking will be done.')
OPT_PROTECTED = PulpCliOption('--protected', d, required=False, parse_func=parsers.parse_boolean)


class CreateOpenstackRepositoryCommand(CreateAndConfigureRepositoryCommand):
    """
    methods relating to repo creation

    Most functionality is handled by the super class
    """

    default_notes = {REPO_NOTE_TYPE_KEY: constants.REPO_NOTE_GLANCE}
    IMPORTER_TYPE_ID = constants.IMPORTER_TYPE_ID

    def __init__(self, context):
        """
        Initialize command.
        """
        super(CreateOpenstackRepositoryCommand, self).__init__(context)
        self.add_option(OPT_AUTO_PUBLISH)
        self.add_option(OPT_PROTECTED)

    def _describe_distributors(self, user_input):
        """
        Subclasses should override this to provide whatever option parsing
        is needed to create distributor configs.

        :param user_input:  dictionary of data passed in by okaara
        :type  user_inpus:  dict

        :return:    list of dict containing distributor_type_id,
                    repo_plugin_config, auto_publish, and distributor_id (the same
                    that would be passed to the RepoDistributorAPI.create call).
        :rtype:     list of dict
        """
        config = {}
        value = user_input.pop(OPT_PROTECTED.keyword, None)
        if value is not None:
            config[constants.CONFIG_KEY_PROTECTED] = value

        auto_publish = user_input.get('auto-publish', True)
        data = [
            dict(distributor_type_id=constants.DISTRIBUTOR_WEB_TYPE_ID,
                 distributor_config=config,
                 auto_publish=auto_publish,
                 distributor_id=constants.CLI_WEB_DISTRIBUTOR_ID),
        ]

        return data

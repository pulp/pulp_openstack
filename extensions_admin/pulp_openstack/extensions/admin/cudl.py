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

# build up options (maybe this should be refactored out, not sure)
d = _('keystone username')
OPT_KEYSTONE_USERNAME = PulpCliOption('--keystone-username', d, required=False)

d = _('keystone password')
OPT_KEYSTONE_PASSWORD = PulpCliOption('--keystone-password', d, required=False)

d = _('keystone URL')
OPT_KEYSTONE_URL = PulpCliOption('--keystone-url', d, required=False)

d = _('keystone tenant')
OPT_KEYSTONE_TENANT = PulpCliOption('--keystone-tenant', d, required=False)


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

        :param context: The client context to use for this command
        :type  context: pulp.client.extensions.core.ClientContext
        """
        super(CreateOpenstackRepositoryCommand, self).__init__(context)
        self.add_option(OPT_AUTO_PUBLISH)
        self.add_option(OPT_PROTECTED)
        self.add_option(OPT_KEYSTONE_USERNAME)
        self.add_option(OPT_KEYSTONE_PASSWORD)
        self.add_option(OPT_KEYSTONE_URL)
        self.add_option(OPT_KEYSTONE_TENANT)

    def _describe_distributors(self, user_input):
        """
        Subclasses should override this to provide whatever option parsing
        is needed to create distributor configs.

        :param user_input:  dictionary of data passed in by okaara
        :type  user_input:  dict

        :return:    list of dict containing distributor_type_id,
                    repo_plugin_config, auto_publish, and distributor_id (the same
                    that would be passed to the RepoDistributorAPI.create call).
        :rtype:     list of dict
        """
        config = {}
        # set up any optional keystone login options
        distributor_opts = [OPT_KEYSTONE_USERNAME, OPT_KEYSTONE_PASSWORD,
                            OPT_KEYSTONE_URL, OPT_KEYSTONE_TENANT]
        for option in distributor_opts:
            value = user_input.pop(option.keyword, None)
            if value is not None:
                config[option.keyword] = value

        value = user_input.pop(OPT_PROTECTED.keyword, None)
        if value is not None:
            config[constants.CONFIG_KEY_PROTECTED] = value

        auto_publish = user_input.get('auto-publish', True)
        data = [
            dict(distributor_type_id=constants.DISTRIBUTOR_WEB_TYPE_ID,
                 distributor_config=config,
                 auto_publish=auto_publish,
                 distributor_id=constants.CLI_WEB_DISTRIBUTOR_ID),
            dict(distributor_type_id=constants.DISTRIBUTOR_GLANCE_TYPE_ID,
                 distributor_config=config,
                 auto_publish=auto_publish,
                 distributor_id=constants.CLI_GLANCE_DISTRIBUTOR_ID),
        ]

        return data

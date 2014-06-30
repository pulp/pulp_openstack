from gettext import gettext as _

from pulp.client.commands.repo import cudl, sync_publish, status
from pulp.client.extensions.decorator import priority

from pulp_openstack.common import constants
from pulp_openstack.extensions.admin.cudl import CreateOpenstackRepositoryCommand
from pulp_openstack.extensions.admin.images import ImageCopyCommand
from pulp_openstack.extensions.admin.images import ImageRemoveCommand
from pulp_openstack.extensions.admin.upload import UploadOpenstackImageCommand
from pulp_openstack.extensions.admin.repo_list import ListOpenstackRepositoriesCommand


SECTION_ROOT = 'openstack'
DESC_ROOT = _('manage Openstack images')

SECTION_REPO = 'repo'
DESC_REPO = _('repository lifecycle commands')

SECTION_UPLOADS = 'uploads'
DESC_UPLOADS = _('upload openstack images into a repository')

SECTION_PUBLISH = 'publish'
DESC_PUBLISH = _('publish a openstack repository')

SECTION_PUBLISH_HTTP = 'http'
DESC_PUBLISH_HTTP = _('publish a openstack repository via http')

SECTION_PUBLISH_GLANCE = 'glance'
DESC_PUBLISH_GLANCE = _('publish a openstack repository via glance')


@priority()
def initialize(context):
    """
    create the openstack CLI section and add it to the root

    :param context: CLI context
    :type  context: pulp.client.extensions.core.ClientContext
    """
    root_section = context.cli.create_section(SECTION_ROOT, DESC_ROOT)
    repo_section = add_repo_section(context, root_section)
    add_upload_section(context, repo_section)
    add_publish_section(context, repo_section)


def add_upload_section(context, parent_section):
    """
    add an upload section to the openstack section

    :param context: pulp context
    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the upload section
                            should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    :return: populated section
    :rtype: PulpCliSection
    """
    upload_section = parent_section.create_subsection(SECTION_UPLOADS, DESC_UPLOADS)
    upload_section.add_command(UploadOpenstackImageCommand(context))

    return upload_section


def add_repo_section(context, parent_section):
    """
    add a repo section to the openstack section

    :param context: pulp context
    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the repo section
                            should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    :return: populated section
    :rtype: PulpCliSection
    """
    repo_section = parent_section.create_subsection(SECTION_REPO, DESC_REPO)

    repo_section.add_command(CreateOpenstackRepositoryCommand(context))
    repo_section.add_command(cudl.DeleteRepositoryCommand(context))
    repo_section.add_command(ImageRemoveCommand(context))
    repo_section.add_command(ImageCopyCommand(context))
    repo_section.add_command(ListOpenstackRepositoriesCommand(context))

    return repo_section


def add_publish_section(context, parent_section):
    """
    add a publish section with subsections to the repo section

    This adds both an "http" and "glance" publish command.

    :param context: pulp context
    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the repo section should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    :return: populated section
    :rtype: PulpCliSection
    """
    publish_section = parent_section.create_subsection(SECTION_PUBLISH, DESC_PUBLISH)

    http_section = publish_section.create_subsection(SECTION_PUBLISH_HTTP, DESC_PUBLISH_HTTP)
    glance_section = publish_section.create_subsection(SECTION_PUBLISH_GLANCE, DESC_PUBLISH_GLANCE)

    renderer = status.PublishStepStatusRenderer(context)
    http_section.add_command(
        sync_publish.RunPublishRepositoryCommand(context,
                                                 renderer,
                                                 constants.CLI_WEB_DISTRIBUTOR_ID))
    http_section.add_command(sync_publish.PublishStatusCommand(context, renderer))

    glance_publish_command = sync_publish.\
        RunPublishRepositoryCommand(context, renderer, constants.CLI_GLANCE_DISTRIBUTOR_ID)

    glance_section.add_command(glance_publish_command)
    glance_section.add_command(sync_publish.PublishStatusCommand(context, renderer))

    return publish_section

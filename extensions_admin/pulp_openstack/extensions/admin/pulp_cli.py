from gettext import gettext as _

from pulp.client.commands.repo import cudl, sync_publish, status
from pulp.client.extensions.decorator import priority

from pulp_openstack.common import constants
from pulp_openstack.extensions.admin.cudl import CreateOpenstackRepositoryCommand
from pulp_openstack.extensions.admin.cudl import UpdateOpenstackRepositoryCommand
from pulp_openstack.extensions.admin.images import ImageCopyCommand
from pulp_openstack.extensions.admin.images import ImageRemoveCommand
from pulp_openstack.extensions.admin.images import ImageSearchCommand
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


@priority()
def initialize(context):
    """
    create the openstack CLI section and add it to the root

    :type  context: pulp.client.extensions.core.ClientContext
    """
    root_section = context.cli.create_section(SECTION_ROOT, DESC_ROOT)
    repo_section = add_repo_section(context, root_section)
    add_upload_section(context, repo_section)
    add_publish_section(context, repo_section)


def add_upload_section(context, parent_section):
    """
    add an upload section to the openstack section

    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the upload section
                            should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    """
    upload_section = parent_section.create_subsection(SECTION_UPLOADS, DESC_UPLOADS)
    upload_section.add_command(UploadOpenstackImageCommand(context))

    return upload_section


def add_repo_section(context, parent_section):
    """
    add a repo section to the openstack section

    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the repo section
                            should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    """
    repo_section = parent_section.create_subsection(SECTION_REPO, DESC_REPO)

    repo_section.add_command(CreateOpenstackRepositoryCommand(context))
    repo_section.add_command(cudl.DeleteRepositoryCommand(context))
    repo_section.add_command(UpdateOpenstackRepositoryCommand(context))
    repo_section.add_command(ImageRemoveCommand(context))
    repo_section.add_command(ImageCopyCommand(context))
    repo_section.add_command(ImageSearchCommand(context))
    repo_section.add_command(ListOpenstackRepositoriesCommand(context))

    return repo_section


def add_publish_section(context, parent_section):
    """
    add a publish section to the repo section

    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the repo section should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    """
    section = parent_section.create_subsection(SECTION_PUBLISH, DESC_PUBLISH)

    renderer = status.PublishStepStatusRenderer(context)
    section.add_command(
        sync_publish.RunPublishRepositoryCommand(context,
                                                 renderer,
                                                 constants.CLI_WEB_DISTRIBUTOR_ID))
    section.add_command(
        sync_publish.PublishStatusCommand(context, renderer))

    return section

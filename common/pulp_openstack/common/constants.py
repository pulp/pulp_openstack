
# TODO: not all of these are used, extras need to be removed

IMAGE_TYPE_ID = 'openstack_image'
IMPORTER_TYPE_ID = 'openstack_importer'
IMPORTER_CONFIG_FILE_NAME = 'server/plugins.conf.d/openstack_importer.json'
DISTRIBUTOR_WEB_TYPE_ID = 'openstack_distributor_web'
CLI_WEB_DISTRIBUTOR_ID = 'openstack_web_distributor_name_cli'
CLI_EXPORT_DISTRIBUTOR_ID = 'openstack_export_distributor_name_cli'
DISTRIBUTOR_CONFIG_FILE_NAME = 'server/plugins.conf.d/openstack_distributor.json'
DISTRIBUTOR_EXPORT_CONFIG_FILE_NAME = 'server/plugins.conf.d/openstack_export_distributor.json'

REPO_NOTE_GLANCE = 'openstack-repo'

# Config keys for the distributor plugin conf
CONFIG_KEY_GLANCE_PUBLISH_DIRECTORY = 'openstack_publish_directory'
CONFIG_VALUE_GLANCE_PUBLISH_DIRECTORY = '/var/lib/pulp/published/openstack'
CONFIG_KEY_EXPORT_FILE = 'export_file'

# Config keys for a distributor instance in the database
CONFIG_KEY_REDIRECT_URL = 'redirect-url'
CONFIG_KEY_PROTECTED = 'protected'
CONFIG_KEY_REPO_REGISTRY_ID = 'repo-registry-id'

# Keys that are specified on the repo config
PUBLISH_STEP_WEB_PUBLISHER = 'publish_to_web'
PUBLISH_STEP_OPENSTACK = 'publish_to_openstack'
PUBLISH_STEP_IMAGES = 'publish_images'
PUBLISH_STEP_OVER_HTTP = 'publish_images_over_http'
PUBLISH_STEP_DIRECTORY = 'publish_directory'

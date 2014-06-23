
IMAGE_TYPE_ID = 'openstack_image'
IMPORTER_TYPE_ID = 'openstack_importer'
IMPORTER_CONFIG_RELATIVE_PATH = 'server/plugins.conf.d/openstack_importer.json'
DISTRIBUTOR_WEB_TYPE_ID = 'openstack_distributor_web'
DISTRIBUTOR_GLANCE_TYPE_ID = 'openstack_distributor_glance'
CLI_WEB_DISTRIBUTOR_ID = 'openstack_web_distributor_name_cli'
CLI_GLANCE_DISTRIBUTOR_ID = 'openstack_glance_distributor_name_cli'
DISTRIBUTOR_CONFIG_FILE_NAME = 'server/plugins.conf.d/openstack_distributor.json'

REPO_NOTE_GLANCE = 'openstack-repo'

# Config keys for the distributor plugin conf
CONFIG_KEY_GLANCE_PUBLISH_DIRECTORY = 'openstack_publish_directory'
CONFIG_VALUE_GLANCE_PUBLISH_DIRECTORY = '/var/lib/pulp/published/openstack'

# Config keys for a distributor instance in the database
CONFIG_KEY_REDIRECT_URL = 'redirect-url'
CONFIG_KEY_PROTECTED = 'protected'

# Keys that are specified on the repo config
PUBLISH_STEP_WEB_PUBLISHER = 'publish_to_web'
PUBLISH_STEP_IMAGES = 'publish_images'
PUBLISH_STEP_OVER_HTTP = 'publish_images_over_http'

PUBLISH_STEP_GLANCE_PUBLISHER = 'publish_to_glance'
PUBLISH_STEP_OVER_GLANCE_REST = 'publish_images_over_glance_rest'

import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient

import uuid


def _get_keystone_client():
    keystone_auth_args = {'username': 'admin',
                          'password': '3842daaf2fe24f81',
                          'tenant_name': 'admin',
                          'auth_url': 'http://192.168.122.97:5000/v2.0/'}
    return ksclient.Client(**keystone_auth_args)


def _get_glance_client():
    keystone = _get_keystone_client()
    glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                       endpoint_type='publicURL')
    print "image endpoint from service catalog is %s" % glance_endpoint
    return glclient.Client(glance_endpoint, token=keystone.auth_token)


def create_image(filename, repo_name, name=None, checksum=None, size=None):
    glance = _get_glance_client()
    image_id = str(uuid.uuid4())
    print "image uuid will be %s" % image_id
    # see http://docs.openstack.org/image-guide/content/image-formats.html
    image_args = {'name': name,
                  'container_format': 'bare',
                  'disk_format': 'qcow2',
                  'protected': True,
                  'visibility': 'public',
                  'from_pulp': 'true',
                  'pulp_repo': repo_name}

    image = glance.images.create(**image_args)

    with open(filename, 'rb') as image_file:
        glance.images.upload(image.id, image_file)

    # grab the image metadata, verify checksum
    image = glance.images.get(image.id)
    print "checksum check: %s" % (checksum == image.checksum)
    print "size check: %s" % (size == image.size)


def find_image(repo_name, image_checksum):
    glance = _get_glance_client()
    filters = {'from_pulp': 'true',
               'pulp_repo': repo_name,
               'checksum': image_checksum}
    return glance.images.list(filters=filters)


def delete_image(image):
    glance = _get_glance_client()
    glance.images.update(image.id, protected=False)
    glance.images.delete(image.id)


CIRROS_PATH = '../common/test/data/cirros-0.3.2-x86_64-disk.img'
RHEL_PATH = '/tmp/rhel-guest-image-7.0-20140506.1.x86_64.qcow2'

fake_unit_key = {'image_checksum': '64d7c1cd2b6f60c92c14662941cb7913'}

print "listing images"
for image in find_image("beav_repo", checksum=fake_unit_key['image_checksum']):
    print image

print "creating image"
create_image(CIRROS_PATH, "beav_repo", checksum='64d7c1cd2b6f60c92c14662941cb7913', size=13167616)

print "listing images"
for image in find_image("beav_repo", checksum=fake_unit_key['image_checksum']):
    print image

print "deleting images"

for image in find_image("beav_repo"):
    print "deleting image %s" % image.id
    delete_image(image)

# print "deleting rhel images"
# for image in find_images("beav_repo_rhel"):
#    print "deleting image %s" % image.id
#    delete_image(image)

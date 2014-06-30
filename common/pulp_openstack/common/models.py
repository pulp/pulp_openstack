import os

from pulp_openstack.common import constants


class OpenstackImage(object):
    """
    A model that holds information about images
    """

    TYPE_ID = constants.IMAGE_TYPE_ID

    def __init__(self, image_checksum, properties):
        """
        :param image_checksum:    MD5 sum
        :type  image_checksum:    basestring
        :param properties:        a set of properties relevant to the image
        :type  properties:        dict
        """
        # assemble info for unit_key
        self.image_checksum = image_checksum
        self.metadata = properties

    @property
    def unit_key(self):
        """
        :return:    unit key
        :rtype:     dict
        """
        return {
            'image_checksum': self.image_checksum,
        }

    @property
    def relative_path(self):
        """
        :return:    the relative path to where this image's directory should live
        :rtype:     basestring
        """
        return self.image_checksum

    def init_unit(self, conduit):
        """
        Use the given conduit's init_unit() call to initialize a unit, and
        store the unit as self._unit.

        :param conduit: The conduit to call init_unit() to get a Unit.
        :type  conduit: pulp.plugins.conduits.mixins.AddUnitMixin
        """
        relative_path_with_filename = os.path.join(self.relative_path,
                                                   self.metadata['image_filename'])
        # this wants relpath + filename, not just relpath
        self._unit = conduit.init_unit(self.TYPE_ID, self.unit_key, self.metadata,
                                       relative_path_with_filename)

    def validate(self):
        """
        Validate the checksum and filesize. This throws an exception if things aren't right.
        """
        # TODO: Currently a no-op.
        pass

    @property
    def storage_path(self):
        """
        Return the storage path of the Unit that underlies this image.
        :return: storage path
        :rtype: string
        """
        return self._unit.storage_path

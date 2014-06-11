import hashlib
import os

from pulp.client.commands.repo.upload import UploadCommand

from pulp_openstack.common import constants


class UploadOpenstackImageCommand(UploadCommand):
    def determine_type_id(self, filename, **kwargs):
        """
        We only support one content type, so this always returns that.

        :return: ID of the type of file being uploaded
        :rtype:  str
        """
        return constants.IMAGE_TYPE_ID

    def generate_unit_key_and_metadata(self, filename, **kwargs):
        """
        Generates the unit key and metadata.

        :param filename: full path to the file being uploaded
        :type  filename: str, None

        :param kwargs: arguments passed into the upload call by the user
        :type  kwargs: dict

        :return: tuple of unit key and metadata to upload for the file
        :rtype:  tuple
        """
        checksum = self._find_image_md5sum(filename)
        size = self._find_image_size(filename)
        unit_key = {'image_checksum': checksum,
                    'image_size': size,
                    'image_filename': os.path.basename(filename)}
        metadata = {}

        return unit_key, metadata

    # TODO: these two methods should probably be in platform. They are used by
    # pulp_rpm as well.

    def _find_image_md5sum(self, filename):
        """
        Return an MD5 sum for a given filename. Openstack also uses MD5 sums for
        images, which is why we use it here as well.

        :param filename: full path to the file to checksum
        :type  filename: str, None

        :return:            The file's md5sum
        :rtype:             basestring
        """
        md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def _find_image_size(self, filename):
        """
        Return filesize for a given filename.

        :param filename: full path to the file to get the size of
        :type  filename: str, None

        :return:            The file's size, in Bytes
        :rtype:             int
        """
        with open(filename, 'rb') as f:
            # Calculate the size by seeking to the end to find the file size with tell()
            f.seek(0, 2)
            size = f.tell()
            return size

from gettext import gettext as _
import hashlib
import os

from pulp.client.commands.repo.upload import UploadCommand
from pulp.client.extensions.extensions import PulpCliOption

from pulp_openstack.common import constants

OPTIONS = []
d = _('human-readable image name')
OPTIONS.append(PulpCliOption('--image_name', d, required=True))

d = _('minimum RAM needed to run image')
OPTIONS.append(PulpCliOption('--image_min_ram', d, required=False))

d = _('disk format')
OPTIONS.append(PulpCliOption('--image_disk_format', d, required=False))

d = _('container format')
OPTIONS.append(PulpCliOption('--image_conatiner_format', d, required=False))


class UploadOpenstackImageCommand(UploadCommand):
    """
    Calculates image data

    This mainly just implements generate_unit_key_and_metadata, most
    functionality is handled by super class.
    """

    def __init__(self, context, upload_manager=None, name=None,
                 description=None, method=None, upload_files=True):
        """
        Initialize upload command.

        This adds options to the command; most functionality is handled by the super class.

        See super() class for more detail.
        """

        super(UploadOpenstackImageCommand, self).__init__(context, upload_manager, name='upload',
                                                          description=description,
                                                          method=method, upload_files=upload_files)

        for option in OPTIONS:
            self.add_option(option)

    def determine_type_id(self, filename, **kwargs):
        """
        We only support one content type, so this always returns that.

        :param filename: filename to determine type of (not used)
        :type  filename: string
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
        unit_key = {'image_checksum': checksum}

        # when uploading an image, set protected=True so the image cannot be
        # inadvertantly deleted by glance

        size = self._find_image_size(filename)
        metadata = {'image_protected': True,
                    'image_size': size,
                    'image_filename': os.path.basename(filename)}

        # we dont want to send through every option, just the ones related to images
        for option in OPTIONS:
            if option.keyword in kwargs:
                metadata[option.keyword] = kwargs[option.keyword]

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

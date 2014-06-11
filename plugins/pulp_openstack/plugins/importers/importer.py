from gettext import gettext as _

import os
import shutil
import logging

from pulp.common.config import read_json_config
from pulp.plugins.conduits.mixins import UnitAssociationCriteria
from pulp.plugins.importer import Importer

from pulp_openstack.common import constants, models


_logger = logging.getLogger(__name__)


def entry_point():
    """
    Entry point that pulp platform uses to load the importer
    :return: importer class and its config
    :rtype:  Importer, dict
    """
    plugin_config = read_json_config(constants.IMPORTER_CONFIG_FILE_NAME)
    return OpenstackImageImporter, plugin_config


class OpenstackImageImporter(Importer):
    @classmethod
    def metadata(cls):
        """
        Used by Pulp to classify the capabilities of this importer. The
        following keys must be present in the returned dictionary:

        * id - Programmatic way to refer to this importer. Must be unique
          across all importers. Only letters and underscores are valid.
        * display_name - User-friendly identification of the importer.
        * types - List of all content type IDs that may be imported using this
          importer.

        :return:    keys and values listed above
        :rtype:     dict
        """
        return {
            'id': constants.IMPORTER_TYPE_ID,
            'display_name': _('Openstack Image Importer'),
            'types': [constants.IMAGE_TYPE_ID]
        }

    def upload_unit(self, repo, type_id, unit_key, metadata, file_path, conduit, config):
        """
        Upload a openstack image.
        See super(self.__class__, self).upload_unit() for the docblock explaining this method.
        """
        image = models.OpenstackImage(unit_key['image_checksum'], unit_key['image_size'],
                                      unit_key['image_filename'])
        # not sure if this is the best way to handle init_unit, pulp_docker is a bit different
        image.init_unit(conduit)
        shutil.move(file_path, image.storage_path)

        try:
            # Let's validate the image. This will raise a
            # ValueError if the image does not validate correctly.
            image.validate()
        except ValueError, e:
            # If validation raises a ValueError, we should delete the file and raise
            os.remove(image.storage_path)
            return {'success_flag': False, 'summary': e.message, 'details': None}

        conduit.save_unit(image._unit)
        return {'success_flag': True, 'summary': None, 'details': None}

    def import_units(self, source_repo, dest_repo, import_conduit, config, units=None):
        """
        Import content units into the given repository. This method will be
        called in a number of different situations:
         * A user is attempting to copy a content unit from one repository
           into the repository that uses this importer
         * A user is attempting to add an orphaned unit into a repository.

        This call has two options for handling the requested units:
         * Associate the given units with the destination repository. This will
           link the repository with the existing unit directly; changes to the
           unit will be reflected in all repositories that reference it.
         * Create a new unit and save it to the repository. This would act as
           a deep copy of sorts, creating a unique unit in the database. Keep
           in mind that the unit key must change in order for the unit to
           be considered different than the supplied one.

        The APIs for both approaches are similar to those in the sync conduit.
        In the case of a simple association, the init_unit step can be skipped
        and save_unit simply called on each specified unit.

        The units argument is optional. If None, all units in the source
        repository should be imported. The conduit is used to query for those
        units. If specified, only the units indicated should be imported (this
        is the case where the caller passed a filter to Pulp).

        :param source_repo: metadata describing the repository containing the
               units to import
        :type  source_repo: pulp.plugins.model.Repository

        :param dest_repo: metadata describing the repository to import units
               into
        :type  dest_repo: pulp.plugins.model.Repository

        :param import_conduit: provides access to relevant Pulp functionality
        :type  import_conduit: pulp.plugins.conduits.unit_import.ImportUnitConduit

        :param config: plugin configuration
        :type  config: pulp.plugins.config.PluginCallConfiguration

        :param units: optional list of pre-filtered units to import
        :type  units: list of pulp.plugins.model.Unit

        :return: list of Unit instances that were saved to the destination repository
        :rtype:  list
        """
        if units is None:
            criteria = UnitAssociationCriteria(type_ids=[constants.IMAGE_TYPE_ID])
            units = import_conduit.get_source_units(criteria=criteria)

        for u in units:
            import_conduit.associate_unit(u)

        return units

    def validate_config(self, repo, config):
        """
        We don't have a config yet, so it's always valid
        """
        return True, ''


def get_models(metadata, unit_key, mask_id=''):
    """
    Given some metadata and a unit key, returns model instances to represent
    each layer of the image defined by the unit_key

    :param metadata:    a dictionary where keys are image IDs, and values are
                        dictionaries with keys "parent" and "size", containing
                        values for those two attributes as taken from the docker
                        image metadata.
    :type  metadata:    dict
    :param unit_key:    a dictionary containing the unit key of the youngest
                        child docker image
    :type  unit_key:    dict
    :param mask_id:     The ID of an image that should not be included in the
                        returned models. This image and all of its ancestors
                        will be excluded.
    :type  mask_id:     basestring

    :return:    list of models.OpenstackImage instances
    :rtype:     list
    """
    # TODO: fix this
    images = []
    return images


def save_models(conduit, models):
    """
    Given a collection of models, save them to pulp as Units.

    :param conduit:         the conduit provided by pulp
    :type  conduit:         pulp.plugins.conduits.unit_add.UnitAddConduit
    :param models:          collection of models.OpenstackImage instances to save
    :type  models:          list
    """

    # TODO: fix
    # conduit.save_unit(unit)
    pass

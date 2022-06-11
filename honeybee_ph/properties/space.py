try:
    from typing import Any, Dict
except ImportError:
    pass  # Python 2.7

from honeybee import properties


class SpaceProperties(properties._Properties):
    """Honeybee-PH Space Properties.

    Space properties. This class will be extended by extensions.

    Usage:

    .. code-block:: python

        space = Space()
        space.properties -> SpaceProperties
        space.properties.ph -> SpacePhProperties
        space.properties.energy -> SpaceEnergyProperties
    """

    def to_dict(self, abridged=False, include=None):
        """Convert properties to dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
            include: A list of keys to be included in dictionary.
                If None all the available keys will be included.
        """
        d = {}
        if abridged == False:
            d['type'] = 'SpaceProperties'
        else:
            d['type'] = 'SpacePropertiesAbridged'
        d = self._add_extension_attr_to_dict(d, abridged, include)
        return d

    @classmethod
    def from_dict(cls, _dict={}, _host=None):
        # type: (Dict, Any) -> SpaceProperties
        assert _dict['type'] == 'SpaceProperties', \
            'Expected SpaceProperties. Got {}.'.format(_dict['type'])

        obj = cls(_host)

        return obj

    def add_prefix(self, prefix):
        """Change the identifier extension attributes unique to this object by adding a prefix.

        Notably, this method only adds the prefix to extension attributes that must
        be unique to the Space (eg. single-room HVAC systems) and does not add the
        prefix to attributes that are shared across several Spaces (eg. ConstructionSets).

        Args:
            prefix: Text that will be inserted at the start of extension attribute identifiers.
        """
        self._add_prefix_extension_attr(prefix)

    def reset_to_default(self):
        """Reset the extension properties assigned at the level of this Room to default.

        This typically means erasing any ConstructionSets or ModifierSets assigned
        to this Space among other properties.
        """
        self._reset_extension_attr_to_default()

    def __repr__(self):
        """Properties representation."""
        return '{}: {}'.format(self.__class__.__name__, self.host.display_name)


class SpacePhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

        # TODO: Temporary override until I figure out right right way
        self._v_sup = None
        self._v_eta = None

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> SpacePhProperties
        _host = new_host or self._host
        new_properties_obj = SpacePhProperties(_host)

        new_properties_obj.id_num = self.id_num
        new_properties_obj._v_sup = self._v_sup
        new_properties_obj._v_eta = self._v_eta

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "{}: [host: {}], v_eta={}, v_sup={}".format(self.__class__.__name__, self.host.display_name, self._v_eta, self._v_sup)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}

        if abridged:
            d['type'] = 'SpacePhPropertiesAbridged'
        else:
            d['type'] = 'SpacePhProperties'

        d['id_num'] = self.id_num
        d['_v_sup'] = self._v_sup
        d['_v_eta'] = self._v_eta

        return {'ph': d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> SpacePhProperties
        assert 'SpacePhProperties' in data['type'], \
            'Expected SpacePhProperties. Got {}.'.format(data['type'])
        new_prop = cls(host)

        new_prop.id_num = data['id_num']
        new_prop._v_sup = data['_v_sup']
        new_prop._v_eta = data['_v_eta']

        return new_prop

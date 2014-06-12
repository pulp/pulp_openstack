from gettext import gettext as _

from pulp.common.error_codes import Error

OST1001 = Error("OST1001", _("The url specified for %(field) is missing a scheme. "
                             "The value specified is '%(url)'."), ['field', 'url'])
OST1002 = Error("OST1002", _("The url specified for %(field) is missing a hostname. "
                             "The value specified is '%(url)'."), ['field', 'url'])
OST1003 = Error("OST1003", _("The url specified for %(field) is missing a path. "
                             "The value specified is '%(url)'."), ['field', 'url'])
OST1004 = Error("OST1004", _("The value specified for %(field): '%(value)s' is not boolean."),
                ['field', 'value'])

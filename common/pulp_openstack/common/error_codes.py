from gettext import gettext as _

from pulp.common.error_codes import Error

GLA1001 = Error("GLA1001", _("The url specified for %(field) is missing a scheme. "
                             "The value specified is '%(url)'."), ['field', 'url'])
GLA1002 = Error("GLA1002", _("The url specified for %(field) is missing a hostname. "
                             "The value specified is '%(url)'."), ['field', 'url'])
GLA1003 = Error("GLA1003", _("The url specified for %(field) is missing a path. "
                             "The value specified is '%(url)'."), ['field', 'url'])
GLA1004 = Error("GLA1004", _("The value specified for %(field): '%(value)s' is not boolean."),
                ['field', 'value'])

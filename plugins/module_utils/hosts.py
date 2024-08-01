# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib
import collections
import typing

from ansible.errors import AnsibleError
from ansible.module_utils.common import yaml

from ansible_collections.itential.core.plugins.module_utils import display


def new(spec, hostvars) -> typing.Any:
    """Create a new instance of a host

    The `new` function will dynamically create a new class object and
    instantiate it with the values provided by hostvars.   This will
    take the host properties from inventory and return an immutable
    instance that represents the host based on the host schema.

    Args:
        name (str): The name of the host class schema
        hostvars (dict): A dictionary of variable from the atsk

    Returns:
        An immutable instance that represents the host
    """
    options = spec.get("options")

    values = dict()
    fields = list()

    for field, properties in options.items():

        fields.append(field)
        value = None

        for item in (properties.get("vars") or list()):
            value = hostvars.get(item)
            if value is not None:
                break
        else:
            value = properties.get("default")
            if value is None and properties.get("required") is True:
                raise AnsibleError(f"missing required property: itential_{field}")

        values[field] = value

        if value is not None:
            field_type = properties.get("type") or "str"

            if (field_type == "bool" and isinstance(value, bool)) or \
                (field_type == "int" and isinstance(value, int)) or \
                (field_type == "dict" and isinstance(value, dict)) or \
                (field_type == "list" and isinstance(value, list)) or \
                (field_type == "str" and isinstance(value, str)):
                    values[field] = value
            else:
                raise AnsibleError(f"invalid data type for {field}")

            choices = properties.get("choices")

            if choices and value not in choices:
                raise AnsibleError(
                    f"invalid value for {field}, expected one of {', '.join(choices)}, got {value}"
                )

    name = spec.get("name").title().replace(".", "")

    return collections.namedtuple(name, fields)(**values)

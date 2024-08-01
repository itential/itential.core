# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib

from typing import Any

from ansible.errors import AnsibleError
from ansible.module_utils.common import yaml

from ansible_collections.itential.core.plugins.module_utils import display


def validate(value, option) -> None:
    """ Validates the value conforms to the option schema

    This function will validate the provided value honors the
    option schema.  If the value violates the schema, this function
    will generate an exception.

    Args:
        value (any): The value to validate
        option (dict): The schema used to validate the value

    Returns:
        None
    """
    choices = option.get("choices")
    if choices and value not in choices:
        raise AnsibleError(f"invalid value, expected one of {', '.join(choices)}, got {value}")

    field_type = option.get("type") or "str"

    validatetype(field_type, value)

    if field_type == "list":
        eletype = option.get("elements")
        for ele in value:
            validatetype(eletype, ele)

    suboptions = option.get("suboptions")

    if suboptions is not None:
        if field_type == "dict":
            for key, item in suboptions.items():
                getvalue(value, key, item)
        elif field_type == "list":
            for ele in value:
                for key, item in suboptions.items():
                    getvalue(ele, key, item)

    if value and isinstance(value, dict) and suboptions is not None:
        for key in value:
            if key not in suboptions:
                raise AnsibleError(f"unknown argument: {key}")


def validatetype(fieldtype, value) -> None:
    """Validates the value is the correct type

    This function will check the type of value and raise an error
    if the value is not of the correct type as specified by the
    field type.   Effectively this simply maps a string type name to
    the actual data type of value.

    Args:
        fieldtype (str): The field type to check the against
        value (any): The field value to validate

    Returns:
        None

    Raises:
        AnsibleError: If the value is not the correct field type
    """
    if (fieldtype == "bool" and not isinstance(value, bool)) or \
        (fieldtype == "int" and not isinstance(value, int)) or \
        (fieldtype == "dict" and not isinstance(value, dict)) or \
        (fieldtype == "list" and not isinstance(value, list)) or \
        (fieldtype == "str" and not isinstance(value, str)):
            raise AnsibleError("invalid data type for field")


def getvalue(args, name, opt) -> Any:
    """Gets the value specified by name from args

    This function will get the value specified by name and attempt to find
    in the args.   If the value does not exist, the function will apply
    the default and check if it is required.

    The function will return the value from args or None if it does
    not exist and is not required.

    Args:
        args (dict): A dictionary object that contains the values
        name (str): The name of the value to retrieve from `args`

    Returns:
        Either the value from `args`, a default value or None

    Raises:
        AnsibleError: When a required value is not present or a value
            is of the wrong type.
    """
    value = args.get(name)

    if value is None:
        for ele in opt.get("aliases") or []:
            value = args.get(ele)
            if value is not None:
                break

    if value is None and opt.get("default") is not None:
        value = opt.get("default")

    if not value and opt.get("required"):
        raise AnsibleError(f"missing required argument: {name}")

    if value is not None:
        try:
            validate(value, opt)
        except AnsibleError as exc:
            display.vvv(str(exc))
            raise exc

    return value


def get(name, task) -> Any:
    """Retrieves the value of an argument from the task.

    The get function will retrieve the value of a module argument that was
    passed in from the playbook.  It wil validate the value is valid per the
    module `options` configuration.   If the value is valid, it will be
    returned to the calling function.  If the value is not valie, this
    function will raise an error.

    Args:
        name (str): The name of the argument to return the value for
        task (ansible.playbook.task.Task): The playbook task instance

    Returns:
        The valuefor the specified argument from the task

    Raises:
        AnsibleError: If the value is not valid
    """
    tokens = task.action.split(".")
    mod = importlib.import_module(f"ansible_collections.{tokens[0]}.{tokens[1]}.plugins.modules.{tokens[2]}")

    docs = yaml.yaml_load(mod.DOCUMENTATION)

    options = docs.get("options") or {}

    opt = options.get(name)

    if not opt:
        raise AnsibleError(f"invalid argument: {name}")

    # construct a set of valid arguments which includes the option key and
    # any configured aliases
    valid_arguments = set()

    for key, value in options.items():
        valid_arguments.add(key)
        for item in value.get("aliases") or []:
            valid_arguments.add(item)

    for key in task.args:
        if key not in valid_arguments:
            display.v(f"key is {key}")
            raise AnsibleError(f"invalid argument: {key}")

    return getvalue(task.args, name, opt)

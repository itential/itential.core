# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib

from ansible.errors import AnsibleError
from ansible.module_utils.common import yaml

from ansible_collections.itential.core.plugins.module_utils import args
from ansible_collections.itential.core.plugins.module_utils import display


def get(task) -> dict:
    """ Returns the module based on the spec

    This function will load the module spec from the a collection and
    return the spec as a Python dict object.

    Args:
        task (str): Python package that represents the module

    Returns:
        The module specification as a dictionary
    """
    tokens = task.action.split(".")
    mod = importlib.import_module(f"ansible_collections.{tokens[0]}.{tokens[1]}.plugins.modules.{tokens[2]}")

    docs = yaml.yaml_load(mod.DOCUMENTATION)

    options = docs.get("options") or {}

    module = {}

    for item in options:
        module[item] = args.get(item, task)

    return module

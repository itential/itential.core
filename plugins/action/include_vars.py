# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import json

from os import listdir
from os.path import isfile, join

from ansible.module_utils.common import yaml

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError

from ansible_collections.itential.core.plugins.module_utils import display
from ansible_collections.itential.core.plugins.module_utils import module


class ActionModule(ActionBase):

    _supports_check_mode = True
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        result = {"changed": False}

        args = module.get(self._task)

        name = args["name"]
        path = args["path"]

        files = [f for f in listdir(path) if self.isvalid(join(path, f))]

        data = list()

        for f in files:
            with open(join(path, f)) as fh:
                contents = fh.read()
                display.v(contents)

                try:
                    loaded = json.loads(contents)
                except Exception as exc:
                    raise
                    try:
                        loaded = yaml.yaml_load(contents)
                    except:
                        raise AnsibleError(f"failed to load file {f}")

                if isinstance(loaded, list):
                    data.extend(loaded)
                else:
                    data.append(loaded)

        result["ansible_facts"] = {name: data}

        return result

    def isvalid(self, f) -> bool:
        """ Checks the path identified by f and returns if it is valid or not

        This function will check the file identified by f for the
        connections.

        1. Is f a file?
        2. Is the file extenson one of `json`, `yaml`, `yml`

        If both conditions are true, the method will return True or
        if one of the conditions is false, the method willr eturn False.

        Args:
            f (str): The filename t check.  Can either an absolute or
                relative path

        Returns:
            A boolean indiciation if the file meets the criteria
        """
        if isfile(f):
            _, ext = os.path.splitext(f)
            return ext in (".json", ".yaml", ".yml")
        return false

#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.core.include_vars
author: Itential

short_description: Load variables from a directory of files

description:
  - The M(itential.core.include_vars) module will taka a source
    path and load all JSON and YAML files.  It will return the
    data as an array.

options:
  name:
    description:
      - The name of the collection
    type: str
    required: true

  path:
    description:
      - The path to load the files from
    type: str
    required: true
"""


EXAMPLES = """
- name: Include all files from config
  itential.core.include_vars:
    name: config
    path: path/to/files
"""

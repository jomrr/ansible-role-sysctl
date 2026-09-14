#!/usr/bin/python
"""Inspect sysctl availability without opening kernel parameters for writing."""

from __future__ import annotations

import os

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
module: sysctl_available
short_description: Inspect sysctl paths before generating configuration
description:
  - Check requested parameters for existing files and effective write access in /proc/sys.
  - Return available and unavailable keys without writing kernel parameters.
  - Checks include file permissions and read-only mounts, but not value-specific kernel restrictions.
author:
  - Jonas Mauer
options:
  keys:
    description: Requested sysctl parameter names in dotted or slash-separated notation.
    type: list
    elements: str
    required: true
  ignore_unavailable:
    description: Return unavailable parameters instead of failing the availability check.
    type: bool
    default: true
attributes:
  check_mode:
    support: full
  diff_mode:
    support: none
"""

EXAMPLES = r"""
- name: SYSCTL | Inspect requested kernel parameters
  become: true
  become_user: root
  sysctl_available:
    keys:
      - net.ipv4.tcp_syncookies
      - kernel.kexec_load_disabled
    ignore_unavailable: true
  register: __sysctl_available
"""

RETURN = r"""
available:
  description: Requested keys with existing, writable sysctl paths.
  type: list
  elements: str
  returned: always
unavailable:
  description: Requested keys with missing or write-protected sysctl paths.
  type: list
  elements: str
  returned: always
"""


def sysctl_path(key: str) -> str:
    """Map sysctl notation to a proc path, preserving dots in interface names."""
    relative = key
    if "." in key and ("/" not in key or key.index(".") < key.index("/")):
        relative = key.translate(str.maketrans("./", "/."))
    return "/proc/sys/" + relative


def inspect_keys(keys: list[str]) -> tuple[list[str], list[str]]:
    """Partition keys using the effective credentials of the applying task."""
    available = []
    unavailable = []
    for key in dict.fromkeys(keys):
        path = sysctl_path(key)
        if os.path.isfile(path) and os.access(path, os.W_OK, effective_ids=True):
            available.append(key)
        else:
            unavailable.append(key)
    return available, unavailable


def main() -> None:
    """Expose availability to Ansible, including in check mode."""
    module = AnsibleModule(
        argument_spec={
            "keys": {"type": "list", "elements": "str", "required": True},
            "ignore_unavailable": {"type": "bool", "default": True},
        },
        supports_check_mode=True,
    )
    available, unavailable = inspect_keys(module.params["keys"])
    if unavailable and not module.params["ignore_unavailable"]:
        module.fail_json(
            msg="Unavailable sysctl parameters: " + ", ".join(unavailable),
            changed=False,
            available=available,
            unavailable=unavailable,
        )
    module.exit_json(changed=False, available=available, unavailable=unavailable)


if __name__ == "__main__":
    main()

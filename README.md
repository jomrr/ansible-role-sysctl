# ansible-role-sysctl

![GitHub](https://img.shields.io/github/license/jam82/ansible-role-sysctl) [![Build Status](https://travis-ci.org/jam82/ansible-role-sysctl.svg?branch=main)](https://travis-ci.org/jam82/ansible-role-sysctl)

**Ansible role for configuring sysctl settings.**

## Supported Platforms

- Alpine 3.12, 3.13
- Archlinux
- CentOS 7, 8
- Debian 10,11
- Fedora 33
- Manjaro
- Oracle 7, 8
- OpenSuse Leap 15.x, Tumbleweed
- Ubuntu 18.04, 20.04

## Requirements

Ansible 2.9 or higher is recommended.

## Variables

Variables and defaults for this role.

### defaults/main.yml

```yaml
sysctl_role_enabled: false
```

## Dependencies

None.

## Example Playbook

```yaml
---
# role: ansible-role-sysctl
# file: site.yml

- hosts: sysctl_systems
  become: true
  gather_facts: true
  vars:
    sysctl_role_enabled: true
  roles:
    - role: ansible-role-sysctl
```

## License and Author

- Author:: [jam82](https://github.com/jam82/)
- Copyright:: 2021, [jam82](https://github.com/jam82/)

Licensed under [MIT License](https://opensource.org/licenses/MIT).
See [LICENSE](https://github.com/jam82/ansible-role-sysctl/blob/master/LICENSE) file in repository.

## References

- [ArchWiki](https://wiki.archlinux.org/)

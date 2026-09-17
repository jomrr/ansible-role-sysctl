# Ansible Role: sysctl

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-sysctl)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-sysctl)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-sysctl)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-sysctl/dev.yml?branch=dev&label=dev)](https://github.com/jomrr/ansible-role-sysctl/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-sysctl/main.yml?branch=main&label=main)](https://github.com/jomrr/ansible-role-sysctl/actions/workflows/main.yml?query=branch%3Amain)

Ansible role for configuring sysctl settings.

## Purpose

Persist kernel hardening settings in seven sysctl.d files and apply the
parameters available in the current namespace. Before writing configuration,
the role checks each requested /proc/sys path for existence and write access
with the privileges used to apply settings. Missing and write-protected
parameters are omitted by default. With sysctl_ignore_unavailable set to false,
the role fails before writing configuration if any parameter is unavailable.
Invalid writable values fail when applied.
The role is idempotent: unchanged configuration does not trigger a reload.

## Scope

### Managed

- Kernel configuration utilities, root-owned configuration files and reloads
  after configuration changes.

### Not Managed

- Resetting undeclared kernel parameters or continuously correcting runtime
  drift between configuration changes.

## Requirements

- systemd-sysctl version 252 or newer, supplied by the supported distributions,
  for strict application of the filtered settings.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
```

## Role Variables

### `sysctl_backup`

Type: `bool`. Required: `false`.

Back up managed configuration files before replacing their contents.

Default:

```yaml
sysctl_backup: true
```

### `sysctl_ignore_unavailable`

Type: `bool`. Required: `false`.

Omit missing or write-protected parameters before writing configuration; false
fails the availability check instead.

Default:

```yaml
sysctl_ignore_unavailable: true
```

### `sysctl_d`

Type: `list`. Required: `false`.

Configuration files managed in /etc/sysctl.d with root ownership and mode 0600.
The default seven hardening files and their 38 settings are defined in
defaults/main.yml.

Default:

```yaml
sysctl_d:
  - file: 90-harden-dev-tty.conf
    settings:
      dev.tty.ldisc_autoload: 0
  - file: 90-harden-fs.conf
    settings:
      fs.protected_fifos: 2
      fs.protected_hardlinks: 1
      fs.protected_regular: 2
      fs.protected_symlinks: 1
  - file: 90-harden-kernel.conf
    settings:
      kernel.dmesg_restrict: 1
      kernel.kexec_load_disabled: 1
      kernel.kptr_restrict: 2
      kernel.perf_event_paranoid: 3
      kernel.printk: 3 3 3 3
      kernel.randomize_va_space: 2
      kernel.sysrq: 0
      kernel.unprivileged_bpf_disabled: 1
      kernel.yama.ptrace_scope: 2
  - file: 90-harden-net-core.conf
    settings:
      net.core.bpf_jit_harden: 2
  - file: 90-harden-vm.conf
    settings:
      vm.mmap_rnd_bits: 32
      vm.mmap_rnd_compat_bits: 16
      vm.unprivileged_userfaultfd: 0
  - file: 90-harden-net-ipv4.conf
    settings:
      net.ipv4.conf.all.accept_redirects: 0
      net.ipv4.conf.all.accept_source_route: 0
      net.ipv4.conf.all.rp_filter: 1
      net.ipv4.conf.all.secure_redirects: 0
      net.ipv4.conf.all.send_redirects: 0
      net.ipv4.conf.default.accept_redirects: 0
      net.ipv4.conf.default.accept_source_route: 0
      net.ipv4.conf.default.rp_filter: 2
      net.ipv4.conf.default.secure_redirects: 0
      net.ipv4.conf.default.send_redirects: 0
      net.ipv4.tcp_rfc1337: 1
      net.ipv4.tcp_syncookies: 1
  - file: 90-harden-net-ipv6.conf
    settings:
      net.ipv6.conf.all.accept_ra: 0
      net.ipv6.conf.all.accept_redirects: 0
      net.ipv6.conf.all.accept_source_route: 0
      net.ipv6.conf.all.use_tempaddr: 2
      net.ipv6.conf.default.accept_ra: 0
      net.ipv6.conf.default.accept_redirects: 0
      net.ipv6.conf.default.accept_source_route: 0
      net.ipv6.conf.default.use_tempaddr: 0
```

## Managed Files

- `/etc/sysctl.d/90-harden-dev-tty.conf` Disable TTY line discipline autoload.
- `/etc/sysctl.d/90-harden-fs.conf` Protect filesystem objects.
- `/etc/sysctl.d/90-harden-kernel.conf` Configure kernel self-protection.
- `/etc/sysctl.d/90-harden-net-core.conf` Harden the BPF JIT.
- `/etc/sysctl.d/90-harden-vm.conf` Randomize mappings and disable unprivileged
  userfaultfd.
- `/etc/sysctl.d/90-harden-net-ipv4.conf` Harden IPv4 processing.
- `/etc/sysctl.d/90-harden-net-ipv6.conf` Harden IPv6 processing without
  disabling IPv6.

## Check Mode

Predict package and configuration changes without writing kernel parameters;
reload handlers are skipped.

- No complete native validation without writes is available; sysctl --dry-run
  does not validate kernel value ranges.

## Service Behavior

Changed files notify one reload handler. systemd-sysctl applies only the
managed sysctl.d files in filename order. No daemon restart is needed.

### Handlers

- SYSCTL | Apply managed kernel settings

## Security Notes

- All managed configuration files are owned by root with mode 0600 and use
  module-provided backups by default.
- Setting kernel.kexec_load_disabled and kernel.unprivileged_bpf_disabled to 1
  cannot be undone before reboot.

## Operational Notes

- At boot, sysctl.d files are sorted lexicographically across directories.
  Identical filenames in /etc take precedence over /run and vendor directories.
  Later files may override these settings. The role reloads only its managed
  files.
- Availability checks cover missing paths, file permissions and read-only
  mounts. Kernel restrictions specific to a value and changes after the check
  can still cause application to fail. Rerun the role when namespace
  availability changes.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Suse | OpenSuse Tumbleweed | latest | [jomrr/molecule-opensuse-tumbleweed:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-tumbleweed) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Apply the default hardening files

Install the seven default files and apply available namespace parameters.

```yaml
---
- name: Configure kernel hardening
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.sysctl
```

### Define custom settings

Replace the default file list with a custom sysctl.d file.

```yaml
---
- name: Configure custom kernel settings
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.sysctl
      sysctl_d:
        - file: 90-custom.conf
          settings:
            net.ipv4.tcp_syncookies: 1
            net.ipv4.ip_forward: 1
```

## References

- [systemd-sysctl](https://www.freedesktop.org/software/systemd/man/latest/systemd-sysctl.service.html)
- [sysctl.d precedence](https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html)

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2021-2024 Jonas Mauer.

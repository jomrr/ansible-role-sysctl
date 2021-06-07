# ansible-role-sysctl

![GitHub](https://img.shields.io/github/license/jam82/ansible-role-sysctl) [![Build Status](https://travis-ci.org/jam82/ansible-role-sysctl.svg?branch=main)](https://travis-ci.org/jam82/ansible-role-sysctl)

**Ansible role for configuring sysctl settings.**

## Supported Platforms

- Alpine
- Archlinux
- CentOS
- Debian
- Fedora
- Manjaro
- OracleLinux
- OpenSuse Leap, Tumbleweed
- Ubuntu

## Requirements

Ansible 2.9 or higher is recommended.

## Variables

Variables and defaults for this role.

### defaults/main.yml

```yaml
# The role is disabled by default, so you do not get in trouble.
# Checked in tasks/main.yml which uses a tasks block if enabled.
sysctl_role_enabled: false

# Backup sysctl config files
sysctl_backup: yes

# Settings for /etc/sysctl.conf. These setting always take precedence
# over sysctl.d config files, load order is:
# - /run/sysctl.d/*.conf
# - /etc/sysctl.d/*.conf
# - /usr/local/lib/sysctl.d/*.conf
# - /usr/lib/sysctl.d/*.conf
# - /lib/sysctl.d/*.conf
# - /etc/sysctl.conf
sysctl_conf:
  kernel.core_uses_pid: 1
  kernel.ctrl-alt-del: 0
  kernel.dmesg_restrict: 1
  kernel.kptr_restrict: 2
  kernel.maps_protect: 1
  kernel.panic: 60
  kernel.panic_on_oops: 60
  kernel.perf_event_paranoid: 3
  kernel.randomize_va_space: 2
  kernel.sysrq: 0
  kernel.unprivileged_bpf_disabled: 1
  kernel.unprivileged_userns_clone: 1
  kernel.yama.ptrace_scope: 2

# Config files in /etc/sysctl.d/*.
sysctl_d:
  # basic ipv4 settings and hardening
  - file: 98-ipv4.conf
    settings:
      net.ipv4.conf.all.accept_redirects: 0
      net.ipv4.conf.all.accept_source_route: 0
      net.ipv4.conf.all.bootp_relay: 0
      net.ipv4.conf.all.forwarding: 0
      net.ipv4.conf.all.proxy_arp: 0
      net.ipv4.conf.all.rp_filter: 1
      net.ipv4.conf.all.secure_redirects: 0
      net.ipv4.conf.all.send_redirects: 0
      net.ipv4.icmp_echo_ignore_broadcasts: 1
      net.ipv4.icmp_ignore_bogus_error_responses: 1
      net.ipv4.ip_forward: 0
      net.ipv4.tcp_fastopen: 3
      net.ipv4.tcp_fin_timeout: 15
      net.ipv4.tcp_invalid_ratelimit: 500
      net.ipv4.tcp_rfc1337: 1
      net.ipv4.tcp_syn_retries: 5
      net.ipv4.tcp_synack_retries: 2
      net.ipv4.tcp_syncookies: 1
      net.ipv4.tcp_timestamps: 1
      net.ipv4.tcp_tw_reuse: 1
  # basic IPv6 settings and hardening, default=disabled
  # enable ipv6 on loopback interface for compatibility (e.g. freeipa)
  - file: 98-ipv6.conf
    settings:
      net.ipv6.conf.lo.disable_ipv6: 0
      net.ipv6.conf.all.disable_ipv6: 1
      net.ipv6.conf.all.accept_ra_defrtr: 0
      net.ipv6.conf.all.accept_ra_pinfo: 0
      net.ipv6.conf.all.accept_ra_rtr_pref: 0
      net.ipv6.conf.all.accept_ra: 0
      net.ipv6.conf.all.accept_redirects: 0
      net.ipv6.conf.all.accept_source_route: 0
      net.ipv6.conf.all.autoconf: 0
      net.ipv6.conf.all.dad_transmits: 0
      net.ipv6.conf.all.forwarding: 0
      net.ipv6.conf.all.max_addresses: 1
      net.ipv6.conf.all.router_solicitations: 0
      net.ipv6.conf.all.use_tempaddr: 2
  # default settings for fs, virutal memory...
  - file: 99-sysctl.conf
    settings:
      dev.tty.ldisc_autoload: 0
      fs.protected_fifos: 2
      fs.protected_hardlinks: 1
      fs.protected_symlinks: 1
      fs.suid_dumpable: 0
      vm.dirty_background_ratio: 5
      vm.dirty_ratio: 30
      vm.min_free_kbytes: 65535
      vm.mmap_min_addr: 4096
      vm.overcommit_memory: 0
      vm.overcommit_ratio: 50
      vm.swappiness: 1
```

## Dependencies

None.

## Example Playbook

```yaml
---
# role: ansible-role-sysctl
# file: site.yml

- hosts: all
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

- [ArchWiki](https://wiki.archlinux.org/index.php/sysctl)
- [Linux Security Guide for Hardening IPv6](https://linux-audit.com/linux-security-guide-for-hardening-ipv6/)

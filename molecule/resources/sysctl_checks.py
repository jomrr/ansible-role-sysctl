"""Exercise hardening and pre-write filtering in an isolated test namespace."""

import os
import sys
from pathlib import Path
from stat import S_IMODE


def prepare() -> None:
    """Seed network values while ensuring host kernel parameters stay protected."""
    assert not os.access('/proc/sys/kernel/kexec_load_disabled', os.W_OK), (
        'A user namespace is required'
    )
    Path('/tmp/molecule-sysctl-kexec-before').write_text(
        Path('/proc/sys/kernel/kexec_load_disabled').read_text(encoding='ascii'), encoding='ascii'
    )
    Path('/proc/sys/net/ipv4/tcp_syncookies').write_text('0\n', encoding='ascii')
    Path('/proc/sys/net/ipv4/conf/all/rp_filter').write_text('0\n', encoding='ascii')
    Path('/proc/sys/net/ipv6/conf/all/accept_ra').write_text('1\n', encoding='ascii')


def verify() -> None:
    """Verify filtered files, permissions, and all active network defaults."""
    assert Path('/proc/sys/kernel/kexec_load_disabled').read_text(encoding='ascii') == (
        Path('/tmp/molecule-sysctl-kexec-before').read_text(encoding='ascii')
    )
    for name in ('dev-tty', 'fs', 'kernel', 'net-core', 'vm', 'net-ipv4', 'net-ipv6'):
        path = Path('/etc/sysctl.d', '90-harden-' + name + '.conf')
        info = path.stat()
        assert info.st_uid == 0 and info.st_gid == 0, path
        assert S_IMODE(info.st_mode) == 0o600, path
    assert 'kernel.kexec_load_disabled=' not in (
        Path('/etc/sysctl.d/90-harden-kernel.conf').read_text(encoding='ascii')
    )
    expected = {
        'net.ipv4.conf.all.accept_redirects': '0',
        'net.ipv4.conf.all.accept_source_route': '0',
        'net.ipv4.conf.all.rp_filter': '1',
        'net.ipv4.conf.all.secure_redirects': '0',
        'net.ipv4.conf.all.send_redirects': '0',
        'net.ipv4.conf.default.accept_redirects': '0',
        'net.ipv4.conf.default.accept_source_route': '0',
        'net.ipv4.conf.default.rp_filter': '2',
        'net.ipv4.conf.default.secure_redirects': '0',
        'net.ipv4.conf.default.send_redirects': '0',
        'net.ipv4.tcp_rfc1337': '1',
        'net.ipv4.tcp_syncookies': '1',
        'net.ipv6.conf.all.accept_ra': '0',
        'net.ipv6.conf.all.accept_redirects': '0',
        'net.ipv6.conf.all.accept_source_route': '0',
        'net.ipv6.conf.all.use_tempaddr': '2',
        'net.ipv6.conf.default.accept_ra': '0',
        'net.ipv6.conf.default.accept_redirects': '0',
        'net.ipv6.conf.default.accept_source_route': '0',
        'net.ipv6.conf.default.use_tempaddr': '0',
    }
    for key, value in expected.items():
        actual = Path('/proc/sys', key.replace('.', '/')).read_text(encoding='ascii').strip()
        assert actual == value, (key, value, actual)
    print(
        'Verified seven files, 20 active network parameters and exclusion of unavailable parameters'
    )


def verify_changed() -> None:
    """Verify an updated sysctl.d file applies only available parameters."""
    content = Path('/etc/sysctl.d/90-harden-net-ipv4.conf').read_text(encoding='ascii')
    assert 'net.ipv4.tcp_syncookies=0' in content
    assert 'net.ipv4.sysctl_molecule_missing' not in content
    assert Path('/proc/sys/net/ipv4/tcp_syncookies').read_text(encoding='ascii').strip() == '0'


if __name__ == '__main__':
    {
        'prepare': prepare,
        'verify': verify,
        'changed': verify_changed,
    }[sys.argv[1]]()

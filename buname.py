#!/usr/bin/env python3

import os
import re
import subprocess
import sys

__version__ = '0.0'
_PROGRAM = 'buname'

_LINUX_DATA = [ (2, 39), (3, 19), (4, 20), (5, 19) ]
_LINUX_ASSUME = 19

def _get_offset(major):
    if major < 3: return None

    offset = 0

    for mj, mn in _LINUX_DATA:
        if mj >= major: break
        offset += mn + 1

    # Extrapolate past last known version
    offset += max(0, major - mj - 1) * (_LINUX_ASSUME + 1)

    return offset

def eternal_2_6(version):
    if type(version) not in (bytes, str):
        raise TypeError('version must be bytes or str')

    pat = r'(\d+)\.(\d+)(.*)'
    if type(version) is bytes:
        pat = pat.encode()

    m = re.fullmatch(pat, version, re.DOTALL)
    if m is None:
        return version

    major, minor, suffix = int(m[1]), int(m[2]), m[3]
    offset = _get_offset(major)

    if offset is None:
        return version
    else:
        prefix = f'2.6.{minor + offset}'
        if type(version) is bytes:
            return prefix.encode() + suffix
        else:
            return prefix + suffix

_ARGS_MAP = {
  'a': 'all',
  's': 'kernel-name',
  'n': 'nodename',
  'r': 'kernel-release',
  'v': 'kernel-version',
  'm': 'machine',
  'p': 'processor',
  'i': 'hardware-platform',
  'o': 'operating-system',
}

_ARGS = list(_ARGS_MAP.values())

def _do_help():
    print("Supported items (see 'uname --help'):")
    for short, long in _ARGS_MAP.items():
        print(f'  -{short}, --{long}')
    print()
    print('Supported options:')
    print('      --help        display this help and exit')
    print('      --version     output version information and exit')

def _do_version():
    print(f'{_PROGRAM} wrapper {__version__}, with data up to Linux {_LINUX_DATA[-1][0] + 1}.x')
    print("See 'uname --version' for more information.")

def _parse_args():
    result = set()

    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]

        if arg == '--':
            i += 1
            if i == len(sys.argv): return result
            break
        elif arg.startswith('--'):
            if arg[2:] in _ARGS:
                result.add(arg[2:])
            elif arg == "--help":
                _do_help()
                sys.exit(0)
            elif arg == "--version":
                _do_version()
                sys.exit(0)
            else:
                print(f"{_PROGRAM}: unrecognized option '{arg}'")
                print(f"Try '{_PROGRAM} --help' and 'uname --help' for more information.")
                sys.exit(1)
        elif arg.startswith('-'):
            for letter in arg[1:]:
                if letter in _ARGS_MAP:
                    result.add(_ARGS_MAP[letter])
                else:
                    print(f"{_PROGRAM}: invalid option -- '{letter}'")
                    print(f"Try '{_PROGRAM} --help' and 'uname --help' for more information.")
                    sys.exit(1)
        else:
            break
    else:
        return result

    print(f"{_PROGRAM}: extra operand '{sys.argv[i]}'")
    print(f"Try '{_PROGRAM} --help' and 'uname --help' for more information.")
    sys.exit(1)

def _call_uname(arg):
    return subprocess.check_output(['uname', '--' + arg]).rstrip(b'\n')

def main():
    parsed = _parse_args()

    if not parsed: parsed.add('kernel-name')

    result = []

    for item in _ARGS:
        if item == 'all': continue

        if item in parsed or 'all' in parsed:
            res = _call_uname(item)

            if item == 'kernel-release':
                res = eternal_2_6(res)
            if item in ('processor', 'hardware-platform'):
                if 'all' in parsed and res == b'unknown':
                    continue

            result.append(res)

    sys.stdout.buffer.write(b' '.join(result))
    sys.stdout.buffer.write(b'\n')

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

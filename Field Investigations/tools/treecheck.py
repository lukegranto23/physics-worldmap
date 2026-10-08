"""Read-only comparison of two frozen output trees; no Git or build execution.

Exit 0: equal under selected policy; 1: different; 2: inspection error.
Symlinks are compared as link text, never followed. Special files are rejected.
This is not a security sandbox or an atomic snapshot of a concurrently changing tree.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat


def manifest(root, *, executable=False):
    root = Path(root).absolute()
    def kind(path):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            return 'symlink', info
        # Reject junctions and non-symlink Windows reparse points.
        if getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError(f'Unsupported reparse point: {path}')
        if stat.S_ISDIR(info.st_mode):
            return 'directory', info
        if stat.S_ISREG(info.st_mode):
            return 'file', info
        raise ValueError(f'Unsupported filesystem object: {path}')

    if kind(root)[0] != 'directory':
        raise ValueError('Each root must be a real directory, not a symlink or file')
    if executable and os.name != 'posix':
        raise ValueError('Executable-bit comparison requires POSIX filesystem semantics')
    entries = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        # Recheck immediately before descent. This is still not a race-proof walk.
        if kind(directory)[0] != 'directory':
            raise ValueError(f'Directory changed during inspection: {directory}')
        for path in sorted(directory.iterdir()):
            entry_type, info = kind(path)
            key = path.relative_to(root).as_posix()
            entry = {'type': entry_type}
            if entry_type == 'directory':
                pending.append(path)
            elif entry_type == 'symlink':
                entry['target'] = os.readlink(path)
            else:
                digest = hashlib.sha256()
                flags = (os.O_RDONLY | getattr(os, 'O_BINARY', 0) |
                         getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
                fd = os.open(path, flags)
                with os.fdopen(fd, 'rb') as stream:
                    before = os.fstat(stream.fileno())
                    if not stat.S_ISREG(before.st_mode):
                        raise ValueError(f'File changed type during inspection: {path}')
                    if (info.st_dev, info.st_ino) != (before.st_dev, before.st_ino):
                        raise ValueError(f'File changed identity during inspection: {path}')
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
                    after = os.fstat(stream.fileno())
                # This Windows runtime returns different ctime semantics through
                # descriptor and pathname stat. Do not mistake that for mutation.
                def fingerprint(s):
                    base = (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
                    return base + ((s.st_ctime_ns,) if os.name == 'posix' else ())
                if fingerprint(before) != fingerprint(after) or fingerprint(after) != fingerprint(path.lstat()):
                    raise ValueError(f'File changed during inspection: {path}')
                entry.update(bytes=after.st_size, sha256=digest.hexdigest())
                if executable:
                    entry['executable'] = bool(after.st_mode & 0o111)
            entries[key] = entry
    return dict(sorted(entries.items()))


def compare(expected, rebuilt, *, executable=False):
    left = manifest(expected, executable=executable)
    right = manifest(rebuilt, executable=executable)
    differences = []
    for path in sorted(set(left) | set(right)):
        if path not in left:
            change = 'added'
        elif path not in right:
            change = 'removed'
        elif left[path] != right[path]:
            change = 'changed'
        else:
            continue
        differences.append({'path': path, 'change': change,
                            'expected': left.get(path), 'rebuilt': right.get(path)})
    return {'equal': not differences, 'policy': {'empty_directories': True,
        'symlinks': 'compare link text, do not follow', 'executable_bit': executable,
        'git_ignore_rules': 'not applied', 'whitespace': 'byte-significant'},
        'expected_entries': len(left), 'rebuilt_entries': len(right),
        'differences': differences}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('expected')
    parser.add_argument('rebuilt')
    parser.add_argument('--check-executable', action='store_true')
    args = parser.parse_args()
    try:
        result = compare(args.expected, args.rebuilt, executable=args.check_executable)
    except (OSError, ValueError) as error:
        print(json.dumps({'error': str(error), 'equal': None}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['equal'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

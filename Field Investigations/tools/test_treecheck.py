"""Local generated fixtures only. No remote calls, dependencies, or builds."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import treecheck


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='treecheck-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.left, self.right = self.root / 'left', self.root / 'right'
        self.left.mkdir()
        self.right.mkdir()

    def pair(self, left=b'baseline\n', right=None):
        (self.left / 'index.js').write_bytes(left)
        (self.right / 'index.js').write_bytes(left if right is None else right)

    def check(self):
        return treecheck.compare(self.left, self.right)

    def test_empty_equal(self):
        self.assertTrue(self.check()['equal'])

    def test_identical_binary(self):
        self.pair(bytes(range(256)))
        self.assertTrue(self.check()['equal'])

    def test_new_untracked_output(self):
        self.pair()
        (self.right / 'new.map').write_bytes(b'map')
        self.assertEqual(self.check()['differences'][0]['change'], 'added')

    def test_removed_stale_output(self):
        self.pair()
        (self.left / '184.index.js').write_bytes(b'old')
        self.assertEqual(self.check()['differences'][0]['change'], 'removed')

    def test_trailing_whitespace(self):
        self.pair(b'left \nright', b'left  \nright')
        self.assertFalse(self.check()['equal'])

    def test_crlf_lf(self):
        self.pair(b'a\r\n', b'a\n')
        self.assertFalse(self.check()['equal'])

    def test_same_size_change(self):
        self.pair(b'abc', b'abd')
        self.assertFalse(self.check()['equal'])

    def test_ignore_rules_not_applied(self):
        for root in (self.left, self.right):
            (root / '.gitignore').write_text('*.secret-test\n')
        (self.right / 'fake.secret-test').write_text('harmless fixture')
        self.assertFalse(self.check()['equal'])

    def test_empty_directory_matters(self):
        (self.left / 'empty').mkdir()
        self.assertFalse(self.check()['equal'])

    def test_file_directory_change(self):
        (self.left / 'item').write_text('file')
        (self.right / 'item').mkdir()
        self.assertEqual(self.check()['differences'][0]['change'], 'changed')

    def test_mtime_ignored(self):
        self.pair()
        os.utime(self.right / 'index.js', (1, 1))
        self.assertTrue(self.check()['equal'])

    def test_missing_root_errors(self):
        with self.assertRaises(OSError):
            treecheck.compare(self.root / 'absent', self.right)

    @unittest.skipUnless(os.name == 'posix', 'POSIX symlink fixture')
    def test_symlinks_not_followed(self):
        for root in (self.left, self.right):
            (root / 'link').symlink_to('../nonexistent')
        self.assertTrue(self.check()['equal'])

    @unittest.skipUnless(os.name == 'posix', 'POSIX symlink fixture')
    def test_symlink_target_change(self):
        (self.left / 'link').symlink_to('../one')
        (self.right / 'link').symlink_to('../two')
        self.assertFalse(self.check()['equal'])

    @unittest.skipUnless(os.name == 'posix', 'POSIX root symlink fixture')
    def test_root_symlink_rejected(self):
        (self.root / 'alias').symlink_to(self.left)
        with self.assertRaises(ValueError):
            treecheck.compare(self.root / 'alias', self.right)

    @unittest.skipUnless(os.name == 'posix', 'POSIX FIFO fixture')
    def test_fifo_rejected_without_reading(self):
        os.mkfifo(self.left / 'pipe')
        with self.assertRaises(ValueError):
            self.check()

    @unittest.skipUnless(os.name == 'posix', 'POSIX executable mode fixture')
    def test_executable_policy(self):
        self.pair()
        os.chmod(self.left / 'index.js', 0o644)
        os.chmod(self.right / 'index.js', 0o755)
        self.assertTrue(self.check()['equal'])
        self.assertFalse(treecheck.compare(self.left, self.right, executable=True)['equal'])

    def test_cli_exit_codes(self):
        args = [sys.executable, str(Path(treecheck.__file__)), str(self.left), str(self.right)]
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)
        self.pair(b'a', b'b')
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 1)
        args[-1] = str(self.root / 'absent')
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 2)


if __name__ == '__main__':
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TreeTests))
    report = {'platform': sys.platform, 'tests_run': result.testsRun,
              'failures': len(result.failures), 'errors': len(result.errors),
              'skipped': len(result.skipped), 'success': result.wasSuccessful(), 'details': stream.getvalue()}
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)

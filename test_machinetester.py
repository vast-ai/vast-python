import unittest
import subprocess  # Add this import
from unittest.mock import patch, MagicMock
import sys
import machinetester  # Assuming machinetester.py is in the same directory

class TestMachineTester(unittest.TestCase):

    def test_is_non_negative_integer(self):
        self.assertTrue(machinetester.is_non_negative_integer('0'))
        self.assertTrue(machinetester.is_non_negative_integer('123'))
        self.assertFalse(machinetester.is_non_negative_integer('-1'))
        self.assertFalse(machinetester.is_non_negative_integer('abc'))
        self.assertFalse(machinetester.is_non_negative_integer('12.3'))

    @patch('machinetester.subprocess.run')
    def test_is_instance_running(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout='{"intended_status": "running"}',
            stderr='',
            returncode=0
        )
        status = machinetester.is_instance('12345')
        self.assertEqual(status, 'running')

    @patch('machinetester.subprocess.run')
    def test_is_instance_unknown(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout='{"intended_status": "unknown"}',
            stderr='',
            returncode=0
        )
        status = machinetester.is_instance('12345')
        self.assertEqual(status, 'unknown')

    @patch('machinetester.subprocess.run')
    def test_is_instance_subprocess_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['./vast', 'show', 'instance', '12345', '--raw'],
            stderr='Error message'
        )
        status = machinetester.is_instance('12345')
        self.assertEqual(status, 'unknown')

    @patch('machinetester.subprocess.run')
    def test_destroy_instance(self, mock_run):
        machinetester.destroy_instance('12345')
        mock_run.assert_called_with(['./vast', 'destroy', 'instance', '12345'])

if __name__ == '__main__':
    unittest.main()

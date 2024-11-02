import unittest
import subprocess  # Add this import
from unittest.mock import patch, MagicMock
import sys
import test  # Assuming test.py is in the same directory

class TestTestPy(unittest.TestCase):

    @patch('test.subprocess.run')
    def test_destroy_instance_with_id(self, mock_run):
        test.instance_id = '12345'
        test.destroy_instance()
        mock_run.assert_called_with(['./vast', 'destroy', 'instance', '12345'])
        self.assertIsNone(test.instance_id)

    @patch('test.subprocess.run')
    def test_destroy_instance_without_id(self, mock_run):
        test.instance_id = None
        test.destroy_instance()
        mock_run.assert_not_called()
        self.assertIsNone(test.instance_id)

    @patch('test.subprocess.run')
    def test_check_requirements_all_met(self, mock_run):
        # Mock successful output from subprocess
        mock_run.return_value = MagicMock(
            stdout='[{"cuda_max_good": "12.5", "reliability": "0.95", "direct_port_count": "4",'
                   '"pcie_bw": "3.0", "inet_down": "100", "inet_up": "100", "gpu_ram": "8"}]',
            stderr='',
            returncode=0
        )
        result = test.check_requirements('12345')
        self.assertTrue(result)

    @patch('test.subprocess.run')
    def test_check_requirements_unmet(self, mock_run):
        # Mock output where requirements are not met
        mock_run.return_value = MagicMock(
            stdout='[{"cuda_max_good": "11.0", "reliability": "0.85", "direct_port_count": "2",'
                   '"pcie_bw": "2.0", "inet_down": "5", "inet_up": "5", "gpu_ram": "6"}]',
            stderr='',
            returncode=0
        )
        with self.assertRaises(SystemExit) as cm:
            test.check_requirements('12345')
        self.assertEqual(cm.exception.code, 1)

    @patch('test.subprocess.run')
    def test_check_requirements_machine_not_found(self, mock_run):
        # Mock empty output indicating machine not found
        mock_run.return_value = MagicMock(
            stdout='[]',
            stderr='',
            returncode=0
        )
        with self.assertRaises(SystemExit) as cm:
            test.check_requirements('12345')
        self.assertEqual(cm.exception.code, 1)

    @patch('test.subprocess.run')
    def test_check_requirements_subprocess_error(self, mock_run):
        # Simulate a subprocess error
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['./vast', 'search', 'offers', 'machine_id=12345', 'verified=any', 'rentable=true', '--raw'],
            stderr='Error message'
        )
        with self.assertRaises(SystemExit) as cm:
            test.check_requirements('12345')
        self.assertEqual(cm.exception.code, 1)

    @patch('test.subprocess.run')
    def test_check_requirements_invalid_json(self, mock_run):
        # Mock invalid JSON output
        mock_run.return_value = MagicMock(
            stdout='Invalid JSON',
            stderr='',
            returncode=0
        )
        with self.assertRaises(SystemExit) as cm:
            test.check_requirements('12345')
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()

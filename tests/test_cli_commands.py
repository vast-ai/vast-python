import unittest
 
from vast import vast

class TestCLICommands(unittest.TestCase):

    def setUp(self):
        self.api_key = 'dummy_api_key'
        self.args = argparse.Namespace()
        self.args.api_key = self.api_key
        self.args.raw = False
        self.args.explain = False

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_put')
    def test_create_instance(self, mock_http_put, mock_apiurl):
        # Setup mock return values
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(status_code=200, json=lambda: {"success": True, "new_contract": 123456})

        # Set command-line arguments
        self.args.ID = 1
        self.args.image = "test_image"
        self.args.env = "VAR1=value1"
        self.args.price = 0.1
        self.args.disk = 10
        self.args.label = "test_label"
        self.args.extra = "extra_info"
        self.args.onstart_cmd = "echo Hello"
        self.args.login = "user"
        self.args.python_utf8 = True
        self.args.lang_utf8 = True
        self.args.jupyter_lab = False
        self.args.jupyter_dir = "/notebooks"
        self.args.force = False
        self.args.cancel_unavail = False
        self.args.template_hash = None
        self.args.args = None

        # Call the function
        vast.create__instance(self.args)

        # Assertions
        mock_http_put.assert_called_once()
        self.assertTrue(mock_http_put.return_value.json()["success"])
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
import argparse
from vast import vast
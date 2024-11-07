import vast
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
from unittest.mock import patch, mock_open, MagicMock
from unittest.mock import patch, MagicMock
import argparse
import unittest

import json
from vast import destroy__instance
import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from vast import create__instance, http_put
import json
import json
from vast import attach__ssh
class TestCLICommands(unittest.TestCase):

    def setUp(self):
        self.args = argparse.Namespace()
        self.args.api_key = 'dummy_api_key'
        self.args.raw = False

    @patch('vast.vast.http_get')
    @patch('vast.vast.http_put')
    @patch('vast.vast.http_post')
    @patch('vast.vast.apiurl')
    def test_create_instance(self, mock_apiurl, mock_http_put, mock_http_post, mock_http_get):
        # Setup args and expected outcomes
        self.args.ID = 1
        self.args.image = "test_image"
        self.args.env = "VAR1=value1"
        self.args.price = 0.1
        self.args.disk = 10
        self.args.label = "test_label"
        self.args.extra = "extra_info"
        self.args.onstart_cmd = "echo Hello"
        self.args.onstart = None
        self.args.entrypoint = None
        self.args.login = "user"
        self.args.python_utf8 = True
        self.args.lang_utf8 = True
        self.args.jupyter_lab = False
        self.args.jupyter_dir = "/notebooks"
        self.args.force = False
        self.args.cancel_unavail = False
        self.args.template_hash = None
        self.args.args = None

        # Mock API URL and HTTP response
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(status_code=200, json=lambda: {"success": True, "new_contract": 123456})

        # Call the function
        vast.create__instance(self.args)

        # Assertions
        mock_apiurl.assert_called_once_with(self.args, "/asks/1/")
        expected_payload = {
            "client_id": "me",
            "image": "test_image",
            "env": {"VAR1": "value1"},
            "price": 0.1,
            "disk": 10,
            "label": "test_label",
            "extra": "extra_info",
            "onstart": "echo Hello",
            "image_login": "user",
            "python_utf8": True,
            "lang_utf8": True,
            "use_jupyter_lab": False,
            "jupyter_dir": "/notebooks",
            "force": False,
            "cancel_unavail": False,
            "template_hash_id": None
        }
        actual_payload = mock_http_put.call_args[1]['json']
        self.assertEqual(actual_payload, expected_payload)

    # Additional tests for other commands would follow a similar structure


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
        self.args.onstart = None
        self.args.entrypoint = None
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

        # Verify the correct URL was constructed
        mock_apiurl.assert_called_once_with(self.args, "/asks/1/")

        # Verify the correct payload was sent
        expected_payload = {
            "client_id": "me",
            "image": "test_image",
            "env": {"VAR1": "value1"},
            "price": 0.1,
            "disk": 10,
            "label": "test_label",
            "extra": "extra_info",
            "onstart": "echo Hello",
            "image_login": "user",
            "python_utf8": True,
            "lang_utf8": True,
            "use_jupyter_lab": False,
            "jupyter_dir": "/notebooks",
            "force": False,
            "cancel_unavail": False,
            "template_hash_id": None
        }
        mock_http_put.assert_called_once()
        actual_payload = mock_http_put.call_args[1]['json']
        self.assertEqual(actual_payload, expected_payload)

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_put')
    def test_destroy_instance(self, mock_http_put, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(status_code=200, json=lambda: {"success": True})
        
        self.args.id = 12345
        vast.destroy__instance(self.args)
        
        mock_apiurl.assert_called_once()
        mock_http_put.assert_called_once()

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_put')
    def test_prepay_instance(self, mock_http_put, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(
            status_code=200, 
            json=lambda: {"success": True, "timescale": 1.0, "discount_rate": 0.2}
        )
        
        self.args.ID = 12345
        self.args.amount = 100.0
        vast.prepay__instance(self.args)
        
        expected_payload = {"amount": 100.0}
        mock_http_put.assert_called_once()
        actual_payload = mock_http_put.call_args[1]['json']
        self.assertEqual(actual_payload, expected_payload)

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_put')
    def test_reboot_instance(self, mock_http_put, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True}
        )
        
        self.args.ID = 12345
        vast.reboot__instance(self.args)
        
        mock_http_put.assert_called_once_with(self.args, "http://mocked.url", headers=vast.headers, json={})

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_put')
    def test_recycle_instance(self, mock_http_put, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True}
        )
        
        self.args.ID = 12345
        vast.recycle__instance(self.args)
        
        mock_http_put.assert_called_once_with(self.args, "http://mocked.url", headers=vast.headers, json={})

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_post')
    def test_search_offers(self, mock_http_post, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"offers": []}
        )
        
        self.args.query = None
        self.args.order = "price"
        self.args.type = "bid"
        self.args.limit = 10
        self.args.storage = 100
        self.args.disable_bundling = False
        self.args.raw = True
        self.args.new = False
        
        vast.search__offers(self.args)
        
        mock_http_post.assert_called_once()
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
import argparse
from vast import vast
 

class TestAttachSSH(unittest.TestCase):
    def setUp(self):
        # Setup base arguments that would come from argparse
        self.args = argparse.Namespace()
        self.args.id = 12345
        self.args.api_key = "test_key"
        self.args.raw = False
        self.args.url = "https://vast.ai/api/v0"
        self.args.ssh_key = "ssh-rsa AAAAB3NzaC1..."

    @patch('vast.http_put')
    def test_attach_ssh_success(self, mock_http_put):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_http_put.return_value = mock_response

        # Call the function
        attach__ssh(self.args)

        # Verify correct URL construction
        expected_url = f"{self.args.url}/instances/{self.args.id}/ssh"
        mock_http_put.assert_called_once()
        actual_url = mock_http_put.call_args[0][1]
        self.assertEqual(actual_url, expected_url)

        # Verify correct payload
        actual_payload = mock_http_put.call_args[1]['json']
        self.assertEqual(actual_payload['ssh_key'], self.args.ssh_key)

    @patch('vast.http_put')
    def test_attach_ssh_raw_output(self, mock_http_put):
        # Test with raw output enabled
        self.args.raw = True
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_http_put.return_value = mock_response

        with patch('builtins.print') as mock_print:
            attach__ssh(self.args)
            mock_print.assert_called_with(json.dumps({"success": True}, indent=1))

    @patch('vast.http_put')
    def test_attach_ssh_error_handling(self, mock_http_put):
        # Test API error handling
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_http_put.return_value = mock_response

        with self.assertRaises(Exception):
            attach__ssh(self.args)

    @patch('vast.http_put')
    def test_attach_ssh_missing_key(self, mock_http_put):
        # Test missing SSH key
        self.args.ssh_key = None
        
        with self.assertRaises(ValueError):
            attach__ssh(self.args)
        
        mock_http_put.assert_not_called()
 

@pytest.fixture
def base_args():
    args = argparse.Namespace()
    args.ID = "12345"
    args.image = "nvidia/cuda:11.0"
    args.env = []
    args.price = 0.4
    args.disk = 10
    args.label = "test-instance"
    args.extra = ""
    args.onstart = None
    args.onstart_cmd = None
    args.entrypoint = "/bin/bash"
    args.login = "root"
    args.python_utf8 = True
    args.lang_utf8 = True
    args.jupyter_lab = False
    args.jupyter_dir = "/workspace"
    args.force = False
    args.cancel_unavail = True
    args.template_hash = None
    args.args = None
    args.raw = False
    args.retry = 3
    args.explain = False
    return args
 

@pytest.mark.parametrize("raw_output", [True, False])
def test_create_instance_basic(base_args, raw_output, capsys):
    base_args.raw = raw_output
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "new_contract": 7835610}
    
    with patch('vast.http_put', return_value=mock_response) as mock_put:
        create__instance(base_args)
        
        # Verify API call
        mock_put.assert_called_once()
        url = mock_put.call_args[0][1]
        payload = mock_put.call_args[1]['json']
        
        # Check URL construction
        assert f"/asks/{base_args.ID}/" in url
        
        # Verify payload
        assert payload['client_id'] == "me"
        assert payload['image'] == base_args.image
        assert payload['price'] == base_args.price
        assert payload['onstart'] == base_args.entrypoint
        
        # Check output format
        captured = capsys.readouterr()
        if raw_output:
            assert json.dumps(mock_response.json(), indent=1) in captured.out
        else:
            assert "Started." in captured.out
 

def test_create_instance_with_onstart_file(base_args):
    onstart_content = "#!/bin/bash\necho hello"
    base_args.onstart = "startup.sh"
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    
    with patch('builtins.open', mock_open(read_data=onstart_content)) as mock_file:
        with patch('vast.http_put', return_value=mock_response) as mock_put:
            create__instance(base_args)
            
            mock_file.assert_called_once_with("startup.sh", "r")
            payload = mock_put.call_args[1]['json']
            assert payload['onstart'] == onstart_content
 

def test_create_instance_with_env_vars(base_args):
    base_args.env = ["KEY1=value1", "KEY2=value2"]
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    
    with patch('vast.http_put', return_value=mock_response) as mock_put:
        create__instance(base_args)
        
        payload = mock_put.call_args[1]['json']
        assert payload['env']['KEY1'] == "value1"
        assert payload['env']['KEY2'] == "value2"
 

def test_create_instance_with_template_hash(base_args):
    base_args.template_hash = "abc123"
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    
    with patch('vast.http_put', return_value=mock_response) as mock_put:
        create__instance(base_args)
        
        payload = mock_put.call_args[1]['json']
        assert payload['template_hash_id'] == "abc123"
        assert 'runtype' not in payload
 

def test_create_instance_explain_mode(base_args, capsys):
    base_args.explain = True
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    
    with patch('vast.http_put', return_value=mock_response):
        create__instance(base_args)
        
        captured = capsys.readouterr()
        assert "request json:" in captured.out
 

class TestDestroyInstance(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace()
        self.args.id = 12345
        self.args.api_key = "test_key"
        self.args.raw = False
        
    @patch('vast.http_delete')
    def test_destroy_instance_success(self, mock_http_delete):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_http_delete.return_value = mock_response
        
        # Execute command
        destroy__instance(self.args)
        
        # Verify correct API call
        mock_http_delete.assert_called_once()
        call_args = mock_http_delete.call_args
        self.assertIn(f"/instances/{self.args.id}/", call_args[0][1])  # Verify URL
        
    @patch('vast.http_delete')
    def test_destroy_instance_api_error(self, mock_http_delete):
        # Setup mock response for API error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_http_delete.return_value = mock_response
        
        # Verify error handling
        with self.assertRaises(Exception):
            destroy__instance(self.args)
            
    @patch('vast.http_delete')
    def test_destroy_instance_raw_output(self, mock_http_delete):
        # Test raw output flag
        self.args.raw = True
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_http_delete.return_value = mock_response
        
        # Capture stdout to verify raw output
        with patch('builtins.print') as mock_print:
            destroy__instance(self.args)
            mock_print.assert_called_with(json.dumps({"success": True}, indent=1))
            
    def test_destroy_instance_invalid_id(self):
        # Test with invalid instance ID
        self.args.id = -1
        with self.assertRaises(ValueError):
            destroy__instance(self.args)
            
    @patch('vast.http_delete')
    def test_destroy_instance_headers(self, mock_http_delete):
        # Verify headers are properly set
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_http_delete.return_value = mock_response
        
        destroy__instance(self.args)
        
        # Verify headers in API call
        call_kwargs = mock_http_delete.call_args[1]
        self.assertIn('headers', call_kwargs)
        self.assertIn('Authorization', call_kwargs['headers'])
        self.assertEqual(call_kwargs['headers']['Authorization'], self.args.api_key)
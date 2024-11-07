
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
    @patch('vast.vast.http_put')
    def test_search_offers(self, mock_http_put, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_put.return_value = MagicMock(
            status_code=200,
            headers={'Content-Type': 'application/json'},
            json=lambda: {"offers": []}
        )
        
        self.args.no_default = False
        self.args.query = None
        self.args.order = ""
        self.args.type = "bid"
        self.args.limit = None
        self.args.storage = None
        self.args.disable_bundling = False
        self.args.new = True
        
        vast.search__offers(self.args)
        
        mock_http_put.assert_called_once()
        actual_payload = mock_http_put.call_args[1]['json']
        self.assertIn('select_cols', actual_payload)
        self.assertIn('q', actual_payload)

    @patch('vast.vast.apiurl')
    @patch('vast.vast.http_get')
    def test_show_machines(self, mock_http_get, mock_apiurl):
        mock_apiurl.return_value = "http://mocked.url"
        mock_http_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"machines": []}
        )
        
        self.args.quiet = False
        vast.show__machines(self.args)
        
        mock_http_get.assert_called_once()
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
import argparse
from vast import vast
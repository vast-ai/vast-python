import unittest
import io
import contextlib
from unittest.mock import patch, MagicMock
from vastai_sdk import VastAI
from vastai_base import VastAIBase


class TestVastAIRealFunctions(unittest.TestCase):
    def setUp(self):
        # Create an instance of VastAI
        self.api_key = 'dummy_api_key'
        self.vast_ai = VastAI(self.api_key)
        self.vast_ai_base = VastAIBase()

    def test_all_imported_methods_are_in_base(self):
        """Check if all dynamically imported methods are declared in VastAIBase. This test case is supposed to prevent the developer from forgetting to declare the methods in the base class."""
        # Now check if each dynamically imported method is declared in the base class
        for method in self.vast_ai.imported_methods:
            # Check if the method exists in VastAIBase as a callable attribute
            # This assumes that VastAIBase should have these methods declared
            self.assertTrue(hasattr(VastAIBase, method) and callable(getattr(VastAIBase, method)),
                            f"VastAIBase should have a method named '{method}'")
    
    def test_all_base_methods_are_in_imported(self):
        """Check if all methods in VastAIBase are dynamically imported methods on VastAI."""
        base_methods = [method for method in dir(VastAIBase) if callable(getattr(VastAIBase, method)) and not method.startswith('__')]
        for method in base_methods:
            self.assertTrue(method in self.vast_ai.imported_methods,
                            f"Method '{method}' declared in VastAIBase should either be present in the dynamically imported methods of VastAI or should be deleted from VastAIBase.")


            

class TestVastAIFakeFunctions(unittest.TestCase):
    def setUp(self):
        # Mock the vast module and its components to avoid actual import and network operations
        self.vast_module_mock = MagicMock()
        self.parser_mock = MagicMock()
        self.subparsers_mock = MagicMock()
        self.subparser_mock = MagicMock()

        # Setup the mock relationships
        self.vast_module_mock.parser = self.parser_mock
        self.parser_mock.subparsers_ = self.subparsers_mock
        self.subparsers_mock.choices = {'command': self.subparser_mock}
        self.subparser_mock.default = MagicMock(return_value="Function Output")
        self.subparser_mock._defaults = {'func': MagicMock(return_value="Function Output")}
        self.subparser_mock._actions = []

        # Prepare to dynamically add a method
        func = MagicMock()
        func.__name__ = "test_function"
        self.subparser_mock.default = func
        self.subparser_mock._defaults = {'func': func}

        # Mock importlib to return the mocked vast module
        patcher = patch('importlib.import_module', return_value=self.vast_module_mock)
        self.addCleanup(patcher.stop)  # Ensure that patcher is stopped after tests
        self.mock_import_module = patcher.start()

        # Create an instance of VastAI
        self.api_key = 'dummy_api_key'
        self.vast_ai = VastAI(self.api_key)

    def test_methods_imported(self):
        """Tests that new function is imported and bound to the VastAI instance."""
        # Check if the method is attached
        self.assertTrue(hasattr(self.vast_ai, 'test_function'), "Method test_function should be dynamically bound to VastAI instances.")
        
        # Check if it's callable
        self.assertTrue(callable(getattr(self.vast_ai, 'test_function')), "test_function should be callable.")

    def test_method_execution(self):
        """Tests that the dynamically imported method can be executed."""
        # Modify the mock to print instead of returning a value
        func = self.subparser_mock._defaults['func']
        func.side_effect = lambda args: print("Function Output")  # This lambda function now prints

        # Now execute the method
        output = self.vast_ai.test_function()
        print(f"Output: {output}")  # Should capture "Function Output"

        # Verify the output
        self.assertEqual(output.strip(), "Function Output", "The test_function should execute and print 'Function Output'.")

    def test_stdout_redirection(self):
        """Tests that stdout is redirected to a buffer."""
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            print("Test output")
            captured = buf.getvalue()
        self.assertEqual(captured.strip(), "Test output")



if __name__ == '__main__':
    unittest.main()

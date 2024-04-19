import importlib
import types
import argparse
from typing import Optional
import io
import contextlib
from vastai_base import VastAIBase


class VastAI(VastAIBase):
    """VastAI SDK class that dynamically imports functions from vast.py and binds them as instance methods.
    
    """
    def __init__(self, api_key, server_url="https://console.vast.ai", retry=3, raw=False, explain=False, quiet=False):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.server_url = server_url
        self.retry = retry
        self.raw = raw
        self.explain = explain
        self.quiet = quiet
        self.imported_methods = {}
        self.import_cli_functions()

    def import_cli_functions(self):
        vast = importlib.import_module("vast")
        parser = vast.parser

        if hasattr(parser, 'subparsers_') and parser.subparsers_:
            for name, subparser in parser.subparsers_.choices.items():
                if name == 'help':
                    continue
                # Attempt to access the default function set by set_defaults
                if hasattr(subparser, 'default') and callable(subparser.default):
                    func = subparser.default
                elif hasattr(subparser, '_defaults') and 'func' in subparser._defaults:
                    func = subparser._defaults['func']
                else:
                    print(f"Command {subparser.prog} does not have an associated function.")
                    continue
                
                func_name = func.__name__.replace('__', '_')
                wrapped_func = self.create_wrapper(func, func_name)
                setattr(self, func_name, types.MethodType(wrapped_func, self))
                # Collect argument details
                arg_details = {}
                if hasattr(subparser, '_actions'):
                    for action in subparser._actions:
                        if action.dest != 'help' and hasattr(action, 'option_strings'):
                            arg_details[action.dest] = {
                                'option_strings': action.option_strings,
                                'help': action.help,
                                'default': action.default,
                                'type': str(action.type) if action.type else None,
                                'required': action.default is None and action.required
                            }

                # Store function with its arguments
                self.imported_methods[func_name] = arg_details
        else:
            print("No subparsers have been configured.")

    def create_wrapper(self, func, method_name):
        """Create a wrapper to check required arguments, convert keyword arguments, and capture output."""
        def wrapper(self, **kwargs):
            required_args = {arg for arg, details in self.imported_methods[method_name].items() if details['required']}
            missing_args = required_args - kwargs.keys()
            if missing_args:
                raise ValueError(f"Missing required arguments for {method_name}: {', '.join(missing_args)}")

            kwargs.setdefault('api_key', self.api_key)
            kwargs.setdefault('url', self.server_url)
            kwargs.setdefault('retry', self.retry)
            kwargs.setdefault('raw', self.raw)
            kwargs.setdefault('explain', self.explain)
            kwargs.setdefault('quiet', self.quiet)
            args = argparse.Namespace(**kwargs)

            # Redirect stdout to capture prints
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                func(args)  # Execute the function, which prints output
                output = buf.getvalue()  # Capture the output

            return output
        
        wrapper.__doc__ = f"Wrapper for {func.__name__}, dynamically imported from vast.py."
        return wrapper
    
    def __getattr__(self, name):
        if name in self.imported_methods:
            return getattr(self, name)
        raise AttributeError(f"{type(self).__name__} has no attribute {name}")
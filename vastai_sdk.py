import importlib
import types
import argparse
from typing import Optional
import io
import contextlib
import requests

from .vastai_base import VastAIBase
from .vast import parser


class VastAI(VastAIBase):
    """VastAI SDK class that dynamically imports functions from vast.py and binds them as instance methods."""

    def __init__(
        self,
        api_key,
        server_url="https://console.vast.ai",
        retry=3,
        raw=False,
        explain=False,
        quiet=False,
    ):
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
        """Dynamically import functions from vast.py and bind them as instance methods."""

        if hasattr(parser, "subparsers_") and parser.subparsers_:
            for name, subparser in parser.subparsers_.choices.items():
                if name == "help":
                    continue
                if hasattr(subparser, "default") and callable(subparser.default):
                    func = subparser.default
                elif hasattr(subparser, "_defaults") and "func" in subparser._defaults:
                    func = subparser._defaults["func"]
                else:
                    print(
                        f"Command {subparser.prog} does not have an associated function."
                    )
                    continue

                func_name = func.__name__.replace("__", "_")
                wrapped_func = self.create_wrapper(func, func_name)
                setattr(self, func_name, types.MethodType(wrapped_func, self))
                arg_details = {}
                if hasattr(subparser, "_actions"):
                    for action in subparser._actions:
                        if action.dest != "help" and hasattr(action, "option_strings"):
                            arg_details[action.dest] = {
                                "option_strings": action.option_strings,
                                "help": action.help,
                                "default": action.default,
                                "type": str(action.type) if action.type else None,
                                "required": action.default is None and action.required,
                                "choices": getattr(
                                    action, "choices", None
                                ),  # Capture choices
                            }

                self.imported_methods[func_name] = arg_details
        else:
            print("No subparsers have been configured.")

    def create_wrapper(self, func, method_name):
        """Create a wrapper to check required arguments, convert keyword arguments, and capture output."""

        def wrapper(self, **kwargs):
            arg_details = self.imported_methods.get(method_name, {})
            for arg, details in arg_details.items():
                if details["required"] and arg not in kwargs:
                    raise ValueError(f"Missing required argument: {arg}")
                if (
                    arg in kwargs
                    and details.get("choices") is not None
                    and kwargs[arg] not in details["choices"]
                ):
                    raise ValueError(
                        f"Invalid choice for {arg}: {kwargs[arg]}. Valid options are {details['choices']}"
                    )
                kwargs.setdefault(arg, details["default"])

            kwargs.setdefault("api_key", self.api_key)
            kwargs.setdefault("url", self.server_url)
            kwargs.setdefault("retry", self.retry)
            kwargs.setdefault("raw", self.raw)
            kwargs.setdefault("explain", self.explain)
            kwargs.setdefault("quiet", self.quiet)

            args = argparse.Namespace(**kwargs)

            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                func(args)  # Execute the function, which prints output
                output = buf.getvalue()  # Capture the output

            return output

        wrapper.__doc__ = (
            f"Wrapper for {func.__name__}, dynamically imported from vast.py."
        )
        return wrapper

    def __getattr__(self, name):
        if name in self.imported_methods:
            return getattr(self, name)
        raise AttributeError(f"{type(self).__name__} has no attribute {name}")

    def _api_request(self, endpoint, params=None):
        """Generic API request handler."""
        url = f"{self.server_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        return response.json()

    def get_gpu_names(self):
        """Returns a set of GPU names available on Vast.ai."""
        endpoint = "/api/v0/gpu_names/unique/"
        gpu_names = self._api_request(endpoint)
        output = set()
        for name in gpu_names["gpu_names"]:
            output.add(name.replace(" ", "_").replace("-", "_"))
        return output

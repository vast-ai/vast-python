#!/usr/bin/env python3

####################################################################################################
# Title: postprocess.py; Author Greg Propf; Date 2022-01-27
####################################################################################################
# A script that scans a python source file and looks for @parser.command blocks.
# It captures these and associates each with a dict key corresponding to the function name. These
# blocks are then further parsed into structured data representing the command-line options for
# each command. Other parts of this script will scan a markdown or html file to determine where the
# function is documented in the file. It will then insert the CL arg docs into that part of the file.
# It's called 'postprocess' because it operates on the files produced by Sphinx that would normally
# be regarded as complete. Ideally this would be integrated into the autodoc workflow but I cannot
# get any of the sphinx modules that are supposed to handle this to work. This is my workaround,
# sacrificing elegance in order to get the job done.
####################################################################################################
import re
import sys

filename = sys.argv[1]
markdown_fname = sys.argv[2]


def parse_cli_block(block):
    cli_arg_dict = dict()
    arg_block_re = re.compile(r'argument\((.*?)\)', re.DOTALL)
    epilog_match = re.search(r'deindent\("""(.*?)"""\)', block, re.DOTALL)
    usage_match = re.search(r'usage="(.+?)"', block)

    args = []
    for match in arg_block_re.finditer(block):
        arg_contents = match.groups()
        args.append(arg_contents)

    if epilog_match is not None and len(epilog_match.groups()) > 0:
        cli_arg_dict["epilog"] = epilog_match.group(1)

    cli_arg_dict["args"] = args

    if usage_match is not None and len(usage_match.groups()) > 0:
        cli_arg_dict["usage"] = usage_match.groups(1)

    return cli_arg_dict


def build_cli_arg_dict(fname):
    with open(fname, "r") as fh:
        source_code = fh.read()
    cli_arguments_block = re.compile(r'@parser.command\((.*?)\)\ndef ([a-z0-9_]+)', re.DOTALL)
    # m = cli_arguments_block.findall(source_code)
    cli_data = dict()
    for match in cli_arguments_block.finditer(source_code):
        cli_args, function_name = match.groups()
        # print ("\n\nCLI STUFF: " + cli_args)
        print("FUNCTION NAME: " + function_name)
        cli_data[function_name] = parse_cli_block(cli_args)
    return cli_data


def interpolate_cli_args_into_markdown(markdown_fname: str, cli_data: dict):
    with open(markdown_fname, "r") as fh:
        markdown_code = fh.read()
    for (func_name, cli_args_block) in cli_data.items():
        print(f"FUNC NAME: {func_name}, CLI_BLOCK: {cli_args_block}")


cli_data = build_cli_arg_dict(filename)
num_funcs = len(cli_data)
print(f"There are {num_funcs} functions in {filename}")
print(repr(cli_data))
print("Now we read the markdown file...")
interpolate_cli_args_into_markdown(markdown_fname, cli_data)
print("DONE!")
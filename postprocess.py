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


def generate_markdown_from_cli_args(cli_dict_for_command):
    """
    Turn the dict into a simple text representation of the cli args and options.

    :param cli_dict_for_command:
    :return str:
    """
    text = ""
    if "usage" in cli_dict_for_command:
        text += "\nusage: " + str(cli_dict_for_command["usage"])
    if "epilog" in cli_dict_for_command:
        text += "\n" + cli_dict_for_command["epilog"]
    if "args" in cli_dict_for_command:
        for arg in cli_dict_for_command["args"]:
            text += f"\n* {arg}"
    return "\n\n" + text


def parse_cli_block(block):
    """
    Goes through the contents of a @parser.command block and extracts
    the components, returning them as a dict.

    :param str block:
    :return Dict:
    """
    cli_arg_dict = dict()
    arg_block_re = re.compile(r'argument\((.*?)\),', re.DOTALL)
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


def build_cli_dict(fname):
    """
    Scans a source code file and builds a dict with a key for each function. The corresponding value is the
    processed @parser.command block for that function.

    :param fname:
    :return Dict:
    """
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
    """
    Iterates through a dict containing the structured cli data for each function. Locates the point in the markdown
    file where each function is documented and inserts our cli docs just before the docs on that function's argument
    list. Returns the modified docs.

    :param str markdown_fname:
    :param Dict cli_data:
    :return str:
    """
    with open(markdown_fname, "r") as fh:
        markdown_code = fh.read()
    for (func_name, cli_args_block) in cli_data.items():
        print(f"FUNC NAME: {func_name}, CLI_BLOCK: {cli_args_block}")
        pattern = "### vast\." + func_name + "(.*?)\* \*\*Parameters\*\*"
        repl_text = f"### vast.{func_name}" + r'\1' + generate_markdown_from_cli_args(
            cli_args_block) + r"\n* **Parameters**"
        markdown_code_with_cli = re.sub(pattern, repl_text, markdown_code, flags=re.DOTALL)
        markdown_code = markdown_code_with_cli
    return markdown_code


cli_dict = build_cli_dict(filename)
num_funcs = len(cli_dict)
print(f"There are {num_funcs} functions in {filename}")
print(repr(cli_dict))
print("Here is the 'search offers' cli text:\n\n")
generate_markdown_from_cli_args(cli_dict["search__offers"])
print("Now we read the markdown file...")
markdown_code_processed = interpolate_cli_args_into_markdown(markdown_fname, cli_dict)

markdown_fname_components = markdown_fname.split(".")
markdown_output_fname = markdown_fname_components[0] + "-processed.md"
with open(markdown_output_fname, "w") as fh:
    fh.write(markdown_code_processed)
print("DONE!")

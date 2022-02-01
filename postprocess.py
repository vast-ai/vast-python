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
import subprocess

script_name = sys.argv[1]
docs_fname = sys.argv[2]



def generate_html_from_cli_args(cli_dict_for_command):
    """
    Turn the dict into an html representation of the cli args and options.

    :param cli_dict_for_command:
    :return str:
    """

    # def arg_md(opt, long_opt, default, help):
    #     return f"*) {opt}, {long_opt}, {help}\n"

    text = ""
    # eval_output = ""
    if "usage" in cli_dict_for_command:
        text += "\n<em>usage: " + str(cli_dict_for_command["usage"]) + "</em><br>\n"
    if "epilog" in cli_dict_for_command:
        pass
        # text += "\n" + cli_dict_for_command["epilog"]
    if "args" in cli_dict_for_command:
        # text += "\n\n<h4>Command Line Options</h4>\n"
        text += "<ul>\n"
        for arg in cli_dict_for_command["args"]:
            text += f"<li>{arg[0]}</li>\n"
            # eval_cmd = f"arg_md({arg[0]})"
            # eval_output = eval(eval_cmd) + "\n"
            # print("EVAL_OUT: " + eval_output)
        text += "</ul>\n"
    # eval(eval_text)
    return "\n\n" + text



def generate_markdown_from_cli_args(cli_dict_for_command):
    """
    Turn the dict into a simple text representation of the cli args and options.

    :param cli_dict_for_command:
    :return str:
    """

    # def arg_md(opt, long_opt, default, help):
    #     return f"*) {opt}, {long_opt}, {help}\n"

    text = ""
    # eval_output = ""
    if "usage" in cli_dict_for_command:
        text += "\nusage: " + str(cli_dict_for_command["usage"])
    if "epilog" in cli_dict_for_command:
        text += "\n" + cli_dict_for_command["epilog"]
    if "args" in cli_dict_for_command:
        text += "\n\n#### Command Line Options\n"
        for arg in cli_dict_for_command["args"]:
            text += f"\n* {arg[0]}"
            # eval_cmd = f"arg_md({arg[0]})"
            # eval_output = eval(eval_cmd) + "\n"
            # print("EVAL_OUT: " + eval_output)

    # eval(eval_text)
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


def underscores_to_dashes(s):
    ttable = s.maketrans("_", "-")
    return s.translate(ttable)


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
        # print("\n\nCLI STUFF: " + cli_args)
        # cmd_components = function_name.split("__")
        # if len(cmd_components) == 2:
        #     [cmd, cmd_target] = cmd_components
        #     cmd_target = underscores_to_dashes(cmd_target)
        #     help_result = subprocess.run(["./vast.py", cmd, cmd_target, "--help"], stdout=subprocess.PIPE)
        #     help_result_text = help_result.stdout.decode('utf-8')
        # print("FUNCTION NAME: " + function_name)
        # cli_data[function_name] = help_result_text
        cli_data[function_name] = parse_cli_block(cli_args)

    return cli_data


def get_processed_doc_fname_and_doc_type(fname):
    fname_components = fname.split(".")
    output_fname = fname_components[0] + "-processed." + fname_components[1]
    return [output_fname, fname_components[1]]


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
            cli_args_block) + r"\n\n\n#### Calling Parameters"
        markdown_code_with_cli = re.sub(pattern, repl_text, markdown_code, flags=re.DOTALL)
        markdown_code = markdown_code_with_cli
    return markdown_code


def interpolate_cli_args_into_html(docs_fname: str, cli_data: dict):
    """
    Iterates through a dict containing the structured cli data for each function. Locates the point in the markdown
    file where each function is documented and inserts our cli docs just before the docs on that function's argument
    list. Returns the modified docs.

    :param str docs_fname:
    :param Dict cli_data:
    :return str:
    """
    with open(docs_fname, "r") as fh:
        html_code = fh.read()
    for (func_name, cli_args_block) in cli_data.items():
        #print(f"FUNC NAME: {func_name}, CLI_BLOCK: {cli_args_block}")

        pattern = f'<span class="pre">vast\.</span></span><span class="sig-name descname"><span class="pre">{func_name}</span>'\
                  + f'(.*?)<dl class="field-list simple">'

        # pattern = "### vast\." + func_name + "(.*?)\* \*\*Parameters\*\*"

        repl_text = f'<span class="pre">vast.</span></span><span class="sig-name descname"><span class="pre">{func_name}</span>'\
                    + r'\1' \
                    + r'<dt class="field-odd">Command Line Parameters</dt>'\
                    + r'<dd class="field-odd"><p>' + generate_html_from_cli_args(cli_args_block)\
                    + r'</p></dd><dl class="field-list simple">'

                    # # '<dl class="field-list simple">'\


        # repl_text = f"### vast.{func_name}" + r'\1' + generate_markdown_from_cli_args(
        #    cli_args_block) + r"\n\n\n#### Calling Parameters"
        html_code = re.sub(pattern, repl_text, html_code, flags=re.DOTALL)
        # html_code = markdown_code_with_cli
    return html_code




cli_dict = build_cli_dict(script_name)
num_funcs = len(cli_dict)
print(f"There are {num_funcs} functions in {script_name}")

[output_fname, output_type] = get_processed_doc_fname_and_doc_type(docs_fname)

if output_type == "html":
    processed_docs = interpolate_cli_args_into_html(docs_fname, cli_dict)
else:
    processed_docs = interpolate_cli_args_into_markdown(docs_fname, cli_dict)

# markdown_fname_components = docs_fname.split(".")
# markdown_output_fname = markdown_fname_components[0] + "-processed.md"
with open(output_fname, "w") as fh:
    fh.write(processed_docs)
print("DONE!")

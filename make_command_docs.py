#!/usr/bin/env python3

####################################################################################################
# Title: make_command_docs.py; Author Greg Propf; Date 2022-02-01
####################################################################################################
# Usage: './make_command_docs' This script runs the 'vast.py' command
# with the --help option to generate the list of commands and then again
# for each command shown by help. It does some minimal formatting on
# the results and produces a Markdown version of the commands and their
# options.
####################################################################################################

import re
import subprocess
import sys

command_headings = dict()

command_headings[('copy')] = "Copy data object from src to dst"
command_headings[('change', 'bid')] = "Change existing bid by id"
command_headings[('create', 'account')] = "Create account (command line account creation no longer supported)"
command_headings[('create', 'instance')] = "Create instance"
command_headings[('destroy', 'instance')] = "Destroy instance"
command_headings[('generate', 'pdf-invoices')] = "Generate pdf-invoices"
command_headings[('label', 'instance')] = "Label instance"
command_headings[('list', 'machine')] = "List machine for rent"
command_headings[('login')] = "Login (command line login no longer supported)"
command_headings[('remove', 'defjob')] = "Remove default job"
command_headings[('scp-url')] = "scp-url"
command_headings[('search', 'offers')] = "Search offers"
command_headings[('set', 'api-key')] = "Set api-key"
command_headings[('set', 'defjob')] = "Set default job"
command_headings[('set', 'min-bid')] = "Set minimum bid"
command_headings[('show', 'instances')] = "Show instances we are renting"
command_headings[('show', 'invoices')] = "Show invoices"
command_headings[('show', 'machines')] = "Show machines we are offering for rent"
command_headings[('show', 'user')] = "Show user account information"
command_headings[('ssh-url')] = "ssh-url"
command_headings[('start', 'instance')] = "Start instance"
command_headings[('stop', 'instance')] = "Stop instance"
command_headings[('unlist', 'machine')] = "Unlist machine"


def snip_lines_from_text(text: str, start_line: int, end_line: int, invert: bool = False):
    text_lines = text.split("\n")
    if invert:
        return text_lines[:start_line] + text_lines[end_line:]
    return text_lines[start_line:end_line]


def make_lines_into_links(text_lines: list):
    return "\n".join([re.sub(r"\s*(.+)\s*", r"[\1](#\1)  ", line) for line in text_lines])


def run_cmd_and_capture_output(verb: str, obj: str = None, direct_obj: str = None) -> str:
    if verb:
        if direct_obj:
            cmd_output = subprocess.run(["./vast.py", verb, obj, direct_obj, "--help"], stdout=subprocess.PIPE)
        elif obj:
            cmd_output = subprocess.run(["./vast.py", verb, obj, "--help"], stdout=subprocess.PIPE)
        else:
            cmd_output = subprocess.run(["./vast.py", verb, "--help"], stdout=subprocess.PIPE)
    else:
        cmd_output = subprocess.run(["./vast.py", "--help"], stdout=subprocess.PIPE)
    cmd_output_text = cmd_output.stdout.decode('utf-8')
    return cmd_output_text


def run_help_for_commands(lines):
    help_text = ""
    lines.sort()
    i = 1
    for line in lines:
        command_parts = re.split(r"\s+", line.strip())
        print(f"{i}: {command_parts}")
        i += 1
        num_command_parts = len(command_parts)
        if num_command_parts == 0:
            continue
        if num_command_parts == 3:
            cmd_output = run_cmd_and_capture_output(command_parts[0], command_parts[1], command_parts[2])
            help_text += f"#### {command_headings[(command_parts[0], command_parts[1], command_parts[2])]}\n\n"
        if num_command_parts == 2:
            cmd_output = run_cmd_and_capture_output(command_parts[0], command_parts[1])
            help_text += f"#### {command_headings[(command_parts[0], command_parts[1])]}\n\n"
        elif num_command_parts == 1:
            cmd_output = run_cmd_and_capture_output(command_parts[0])
            help_text += f"#### {command_headings[(command_parts[0])]}\n\n"
        help_text += f"```\n{cmd_output}\n```\n---\n"

    return help_text


main_help_text = run_cmd_and_capture_output("", "")
# command_index = make_lines_into_links(snip_lines_from_text(main_help_text, 4, 27)) + "\n\n"


main_help_text = run_cmd_and_capture_output("", "")
# main_help_text_lines = main_help_text.split("\n")
snipped_help_text = snip_lines_from_text(main_help_text, 4, 28)
#snipped_help_text = snipped_help_text.sort()
command_help_text = run_help_for_commands(snipped_help_text)
# main_help_text = "\n".join(snip_lines_from_text(main_help_text, 1, 27, True))
main_help_text = f"```\n{main_help_text}\n```\n"


with open("commands.md", "w") as fh:
#    fh.write(command_index)
    fh.write(main_help_text)
    fh.write(command_help_text)

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
    i = 1
    for line in lines:
        cmd_output = ""
        line_parts = re.split(r"\s{2,}", line.strip())
        command_parts = re.split(r"\s+", line_parts[0])
        if len(line_parts) < 2:
            line_parts.append("")
        print(f"{i}: {command_parts}")
        i += 1
        num_command_parts = len(command_parts)
        if num_command_parts == 0:
            continue
        if num_command_parts == 3:
            cmd_output = run_cmd_and_capture_output(command_parts[0], command_parts[1], command_parts[2])
        if num_command_parts == 2:
            cmd_output = run_cmd_and_capture_output(command_parts[0], command_parts[1])
        elif num_command_parts == 1:
            cmd_output = run_cmd_and_capture_output(command_parts[0])

        help_text += f"#### {line_parts[0]} -- {line_parts[1]}\n\n"
        help_text += f"```\n{cmd_output}\n```\n---\n"

    return help_text


main_help_text = run_cmd_and_capture_output("", "")
snipped_help_text = snip_lines_from_text(main_help_text, 4, 29)
snipped_help_text = sorted(list(map(str.strip, snipped_help_text)))

command_help_text = run_help_for_commands(snipped_help_text)
main_help_text = f"```\n{main_help_text}\n```\n"


with open("commands.md", "w") as fh:
    fh.write(main_help_text)
    fh.write(command_help_text)

#!/usr/bin/env python3

####################################################################################################
# Title: make_command_docs.py; Author Greg Propf; Date 2022-02-01
####################################################################################################
# This script runs the 'vast.py' command with the --help option to generate the list of commands
# and then again for each command shown by help. It does some minimal formatting on the results
# and produces a Markdown version of the commands and their options.
####################################################################################################

import re
import subprocess


def run_cmd_and_capture_output(verb: str, obj: str = None) -> str:
    if verb:
        if obj:
            cmd_output = subprocess.run(["./vast.py", verb, obj, "--help"], stdout=subprocess.PIPE)
        else:
            cmd_output = subprocess.run(["./vast.py", verb, "--help"], stdout=subprocess.PIPE)
    else:
        cmd_output = subprocess.run(["./vast.py", "--help"], stdout=subprocess.PIPE)
    cmd_output_text = cmd_output.stdout.decode('utf-8')
    return cmd_output_text


def run_help_for_commands(lines):
    help_text = ""
    for line in lines:
        command_parts = re.split(r"\s+", line.strip())
        print(command_parts)
        num_command_parts = len(command_parts)
        if num_command_parts == 2:
            cmd_output = run_cmd_and_capture_output(command_parts[0], command_parts[1])
            help_text += f"```\n{cmd_output}\n```\n---\n"
        elif num_command_parts == 1:
            cmd_output = run_cmd_and_capture_output(command_parts[0])
            help_text += f"```\n{cmd_output}\n```\n---\n"
        else:
            print("NO COMMAND PRESENT.")
    return help_text


main_help_text = run_cmd_and_capture_output("", "")
main_help_text_lines = main_help_text.split("\n")
main_help_text = f"```\n{main_help_text}\n```\n"
command_help_text = run_help_for_commands(main_help_text_lines[5:28])

with open("commands.md", "w") as fh:
    fh.write(main_help_text)
    fh.write(command_help_text)

#!/usr/bin/env python3

####################################################################################################
# Title: make_command_docs.py; Author Greg Propf; Date 2022-02-01
####################################################################################################
# This script runs the 'vast.py' command with the --help option to generate the list of commands
# and then again for each command shown by help. It does some minimal formatting on the results
# and produces Markdown docs of all the commands and their options.
####################################################################################################

import re
import sys
import subprocess

def run_cmd_and_capture_output(verb: str, obj: str) -> str:
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
        command_parts = re.split(r"\s+", line)
        print(command_parts)
        if len(command_parts) == 3:
            cmd_output = run_cmd_and_capture_output(command_parts[1], command_parts[2])
            cmd_output_lines = cmd_output.split("\n")
            add_markdown(cmd_output_lines)
            help_text += "\n".join(cmd_output_lines)
        elif len(command_parts) == 2:
            cmd_output = run_cmd_and_capture_output(command_parts[1], None)
            cmd_output_lines = cmd_output.split("\n")
            add_markdown(cmd_output_lines)
            help_text += "\n".join(cmd_output_lines)
        else:
            print("NO COMMAND PRESENT.")
        help_text += "---\n"
    return help_text


def add_markdown(lines, main_command_list=False):
    add_linebreak = False
    lines[0] = "_" + lines[0] + "_"
    if main_command_list:
        del lines[2:4]
        lines.insert(2, "\n")
        lines.insert(2, "**Command**")
    i = 0
    for line in lines:
        if re.match("optional arguments", line):
            add_linebreak = True
        if add_linebreak:
            lines[i] += "  "
        i += 1
    if main_command_list:
        lines.append("___\n")
    return lines

main_help_text = run_cmd_and_capture_output("", "")
main_help_text_lines = main_help_text.split("\n")

# print(main_help_text)


add_markdown(main_help_text_lines, True)

command_help_text = run_help_for_commands(main_help_text_lines[5:28])
command_help_text_lines = command_help_text.split("\n")

with open("commands.md", "w") as fh:
    for ln in main_help_text_lines:
        fh.writelines(ln + "\n")
    for ln in command_help_text_lines:
        fh.writelines(ln + "\n")

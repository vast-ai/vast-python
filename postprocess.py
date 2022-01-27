#!/usr/bin/env python3

####################################################################################################
# Title: postprocess.py; Author Greg Propf; Date 2022-01-27
####################################################################################################
# A script that scans a python source file and looks for @parser.command blocks.
# It captures these and associates each with a dict key corresponding to the function name. These
# blocks are then further parsed into structured data representing the command-line options for
# each command. Other parts of this script will scan a markdown or html file to determine where the
# function is documented in the file. It then inserts the CL arg docs into that part of the file.
# It's called 'postprocess' because it operates on the files produces by Sphinx that would normally
# be regarded as complete. Ideally this would be integrated into the autodoc workflow but I cannot
# get any of the sphinx modules that are supposed to handle this to work. This is my workaround,
# sacrificing elegance in order to get the job done.
####################################################################################################
import re
import sys

filename = sys.argv[1]
with open(filename, "r") as fh:
    source_code = fh.read()


test_text = """
@parser.command(
Some args and stuff here,
Some args and stuff here,
Some args and stuff here,
Some args and stuff here,
)
def some__command():
"""

test_text_simple = """
@parser.command(
fdfsdf
sdfsdf
sfsf
)
def foo_bar(a,b,d):
    blah
    blaj
    

@parser.command(
454354543
gqqqqqqqqqqqqqqqq
rrrrrrrrrrrrrrrr
yyyyyyyyyyy
uuuuuuuuuuuuuuu
)
def whobobobob(g,h,j):
    blah
    blaj




"""



# Example: re.compile(r"^(.+)\n((?:\n.+)+)", re.MULTILINE) -- https://stackoverflow.com/questions/587345/regular-expression-matching-a-multiline-block-of-text

#cli_regex = re.compile(r"^@parser.command\($.+\)$def ([a-z0-9]_)+", re.MULTILINE)

cli_regex_simple = re.compile(r'@parser.command\((.*?)\)\ndef ([a-z0-9_]+)',  re.DOTALL)

m = cli_regex_simple.findall(test_text_simple)


#match = re.search(r'parser.commandA.*A', test_text_simple, re.DOTALL)

#match.group(0)
cli_data = dict()

for match in cli_regex_simple.finditer(source_code):
     cli_args, function_name = match.groups()
     #print ("\n\nCLI STUFF: " + cli_args)
     print ("FUNCTION NAME: " + function_name)
     cli_data[function_name] = cli_args

print ("DONE")
print (repr(cli_data))
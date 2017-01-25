#!/usr/bin/env python3
## @package contents
#  extract markdown-like comments from a file and convert them to markdown.
#
# extract markdown-like comments from (source code) file, convert them
# to valid markdown and run pandoc on it.
# Since the comment characters for different languages differ,
# this program can be adjusted to use the comment character used in your
# file by command line arguments.

"""
#######% % markdown comments for various source files
#######% % Dominik Cullmann
#######%
#######% extract markdown-like comments from (source code) file, convert them
#######% to valid markdown and run pandoc on it.
#######% Since the comment characters for different languages differ,
#######% this program can be adjusted to use the comment character used in your
#######% file by command line arguments.
#######%
#######% copyright: 2014-2017, Dominik Cullmann
#######% license: BSD 2-Clause
#######% maintainer: Dominik cullmann
#######% email: dominik.cullmann@forst.bwl.de
#######%
"""

#% import modules
import re
import subprocess
import argparse
import textwrap
import os
import sys

## Test if a Program is Installed
# @param name The name of the program to be tested for.
def is_tool(name):
    """
    test if a program is installed
    """
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name, "-h"], stdout=devnull,
                         stderr=devnull).communicate()
    except OSError:
        print("please install " + name)
        if name == "pandoc" and os.name != "posix":
            print("you may try\n" + 'install.packages("installr"); ' +
                  'library("installr"); install.pandoc()\n' + "in GNU R")
        raise
    return True


## Just a Custom Formatter
#
# Internally used only.
class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    """
    Just a custom formatter.
    """
    pass


## Use a Custom Parser Function
#
# Use a parser function to add argparse help to docstring
# taken from http://stackoverflow.com/questions/22793577/
# display-argparse-help-within-pydoc.
def make_parser():
    """
    Use a parser function to add argparse help to docstring
    taken from http://stackoverflow.com/questions/22793577/
    display-argparse-help-within-pydoc.
    """

    parser = argparse.ArgumentParser(formatter_class=CustomFormatter,
                                     description="convert markdown-style " +
                                     "comments from a file to markdown and " +
                                     "html via pandoc.",
                                     epilog=textwrap.dedent("""\
markdown style comments are headed by one or more comment characters giving
the markdown heading level and a magic character marking it as
markdown.
try --example for an example
            """))
    parser.add_argument("file_name", metavar="file",
                        help="The name of the file to convert comments from.")
    parser.add_argument("-o", "--postfix", dest="name_postfix",
                        default="",
                        help="Change the postfix added to the files created.")
    parser.add_argument("-e", "--prefix", dest="name_prefix",
                        default="",
                        help="Change the prefix added to the files created.")
    parser.add_argument("-c", "--comment", dest="comment_character",
                        default="#",
                        help="Change the comment character.")
    parser.add_argument("-m", "--magic", dest="magic_character",
                        default="%",
                        help="Change the magic character.")
    parser.add_argument("-v", "--version", action="version",
                        version="0.3.0")
    parser.add_argument("-x", "--example", action="version",
                        help="Give an example and exit.",
                        version=("""
##% *This* is an example markdown comment of heading level 2
#######% **This** is an example of a markdown paragraph: markdown recognizes
#######% only six levels of heading, so we use seven levels to mark
#######% "normal" text.
#######% Here you can use the full
#######% [markdown syntax](http://daringfireball.net/projects/markdown/syntax).
#######% *Note* the trailing line: markdown needs an empty line to end a
#######% paragraph.
#######%
"""))
    parser.add_argument("-p", "--pandoc", dest="run_pandoc",
                        help="Run pandoc on the md file created.",
                        action="store_true")
    parser.add_argument("-n", "--no-pandoc", dest="run_pandoc",
                        help="Do not run pandoc on the md file created.",
                        action="store_false")
    parser.add_argument("-l", "--latex", dest="compile_latex",
                        help="Run LaTex on the tex file created via pandoc.",
                        action="store_true")
    parser.add_argument("--no-latex", dest="compile_latex",
                        help="Run LaTex on the tex file created via pandoc.",
                        action="store_false")
    parser.set_defaults(run_pandoc=False, compile_latex=False)
    return parser


#% define parser
## Extract Matching Lines
#
# Extract all lines starting with a combination of comment_character and
# magic_character from a file.
#@ param file_name The file from which the lines are to be extracted.
#@ param comment_character The comment character of the files language ("#" for
# example.
#@ magic_character The magic character marking lines as markdown comments.
def extract_md(file_name, comment_character, magic_character):
    """
    extract all lines starting with a combination of comment_character and
    magic_character.
    """
    matching_lines = []
    markdown_regex = re.compile("\s*" + comment_character + "+" +
                                magic_character)
    infile = open(file_name, "r")
    for line in infile:
        if markdown_regex.match(line):
            matching_lines.append(line)
    infile.close()
    return(matching_lines)


#% define converter
## Convert Lines to Markdown
#
# Remove whitespace and magic characters from lines and output valid markdown.
#@ param file_name The file from which the lines are to be extracted.
#@ param comment_character The comment character of the files language ("#" for
# example.
#@ magic_character The magic character marking lines as markdown comments.
def convert(lines, comment_character, magic_character):
    """
    convert lines to markdown
    """
    converted_lines = []
    for line in lines:
        line = line.lstrip()
        #########% remove 7 or more heading levels.  
        line = re.sub(comment_character + "{7,}", "", line)
        line = line.replace(comment_character, "#")
        if magic_character != "":
            #######% remove the first occurence of the magic_character
            #######% (the header definition of pandoc"s markdown uses the
            #######% percent sign, if that is the magic pattern, all pandoc
            #######% standard headers would end up to be simple text.  
            line = re.sub(magic_character, "", line, count=1)
            # get rid of leading blanks
            line = re.sub("^\s*", "", line)
        #######% empty lines (ending markdown paragraphs) are not written by
        #######% file.write(), so we replace them by newlines.
        #######%
        if line == " " or line == "":
            line = "\n"
        converted_lines.append(line)
    return(converted_lines)

#% write file contents
## Write Table of Contents
#
#@ param file_name The file from which the lines are to be extracted.
#@ param comment_character The comment character of the files language ("#" for
# example.
#@ magic_character The magic character marking lines as markdown comments.
#@ postfix Set the content's file postfix.
#@ prefix Set the content's file prefix.
#@ run_pandoc Run pandoc on the the contents file?
#@ compile_latex Compile the LaTeX file?
def contents(file_name, comment_character, magic_character, postfix,
             prefix, run_pandoc, compile_latex):
    """
    Write table of contents to file
    """
    ##% get matchting lines
    lines_matched = extract_md(file_name=file_name,
                               comment_character=comment_character,
                               magic_character=magic_character)
    ##% convert matched lines to markdown
    markdown_lines = convert(lines=lines_matched,
                             comment_character=comment_character,
                             magic_character=magic_character)
    if all(line == "\n" for line in markdown_lines):
        sys.exit(2)
    ##% write md file
    base_name = os.path.basename(os.path.splitext(file_name)[0])
    full_base_name = prefix + base_name + postfix
    md_file_name = full_base_name + ".md"
    md_file = open(md_file_name, "w")
    for markdown_line in markdown_lines:
        md_file.write(markdown_line)
    md_file.close()
    ##% run pandoc
    if is_tool("pandoc") & run_pandoc:
        subprocess.call(["pandoc", "-N", md_file_name, "-o", full_base_name +
                        ".html"])
        subprocess.call(["pandoc", "-N", md_file_name, "-o", full_base_name +
                        ".pdf"])
        subprocess.call(["pandoc", "-sN", md_file_name, "-o", full_base_name +
                        ".tex"])
        if compile_latex:
            ###% If on posix...
            if os.name == "posix":
                ####% ... tex it
                if is_tool("texi2pdf"):
                    subprocess.call(["texi2pdf", "--batch", "--clean",
                                    full_base_name + ".tex"])
            else:
                ####% ... warn otherwise
                print("you are not running posix, see how to compile\n" +
                      full_base_name + ".tex"
                      "\nconsulting your operating system's documentation.")
    return(0)

_parser = make_parser()
__doc__ += _parser.format_help()

#% main
if __name__ == "__main__":
    ##% parse command line arguments
    args = _parser.parse_args()
    ##% write table of contents to file
    ret = contents(file_name=args.file_name,
                   comment_character=args.comment_character,
                   magic_character=args.magic_character,
                   postfix=args.name_postfix,
                   prefix=args.name_prefix,
                   run_pandoc=args.run_pandoc,
                   compile_latex=args.compile_latex)
    sys.exit(ret)

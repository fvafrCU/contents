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
from __future__ import print_function
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
    Test if a Program is Installed
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


## Use a Custom Parser Function
#
# To keep __main__ tiny.
def make_parser():
    """
    Use a Custom Parser Function

    To keep __main__ tiny.
    """

    parser = argparse.ArgumentParser(description="convert markdown-style " +
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
    parser.add_argument("--formats", dest="pandoc_formats",
                        default=('tex', 'html', 'pdf'),
                        help="Change the comment character.")
    parser.set_defaults(run_pandoc=False, compile_latex=False)
    return parser


## Extract Matching Lines
#
# Extract all lines starting with a combination of comment_character and
# magic_character from a file.
# @param file_name The file from which the lines are to be extracted.
# @param comment_character The comment character of the files language ("#" for
# example.
# @param magic_character The magic character marking lines as markdown
#  comments.
def extract_md(file_name, comment_character, magic_character):
    """
    Extract Matching Lines
    """
    matching_lines = []
    markdown_regex = re.compile(r"\s*" + comment_character + "+" +
                                magic_character)
    infile = open(file_name, "r")
    for line in infile:
        if markdown_regex.match(line):
            matching_lines.append(line)
    infile.close()
    return matching_lines


## Convert Lines to Markdown
#
# Remove whitespace and magic characters from lines and output valid markdown.
# @param lines The lines to be converted.
# @param comment_character The comment character of the files language.
# @param magic_character The magic character marking lines as markdown
#  comments.
def convert(lines, comment_character, magic_character):
    """
    Convert Lines to Markdown
    """
    converted_lines = []
    for line in lines:
        line = line.lstrip()
        # remove 7 or more heading levels.
        line = re.sub(comment_character + "{7,}", "", line)
        line = line.replace(comment_character, "#")
        if magic_character != "":
            # remove the first occurence of the magic_character
            # (the header definition of pandoc's markdown uses the
            # percent sign, if that was the magic pattern, all pandoc
            # standard headers would end up to be simple text.
            line = re.sub(magic_character, "", line, count=1)
            # get rid of leading blanks
            line = re.sub(r"^\s*", "", line)
        # empty lines (ending markdown paragraphs) are not written by
        # file.write(), so we replace them by newlines.
        if line == " " or line == "":
            line = "\n"
        converted_lines.append(line)
    return converted_lines


## Get Table of Contents
#
# Just a wrapper to extract_md() and convert().
# @param file_name The file from which the lines are to be extracted.
# @param comment_character The comment character of the files language ("#" for
#  example).
# @param magic_character The magic character marking lines as markdown
#  comments.
def toc(file_name, comment_character, magic_character):
    """
    Get Table of Contents
    """
    lines_matched = extract_md(file_name=file_name,
                               comment_character=comment_character,
                               magic_character=magic_character)
    converted_lines = convert(lines=lines_matched,
                              comment_character=comment_character,
                              magic_character=magic_character)
    return converted_lines


## Modify a Path
#
# Add a postfix and a prefix to the basename of a path and optionally change
# it's extension.
# @param file_name The file to be modified.
# @param postfix Set the content's file postfix.
# @param prefix Set the content's file prefix.
# @param extension Set a new file extension.
def modify_path(file_name, postfix="", prefix="", extension=None):
    """
    Modify a Path
    """
    if extension is None:
        extension = os.path.splitext(file_name)[1]
    base_name = os.path.basename(os.path.splitext(file_name)[0])
    ext_base_name = prefix + base_name + postfix
    ext = extension.lstrip(".")
    name = os.path.join(os.path.dirname(file_name), ext_base_name) + "." + ext
    return name


## Run Pandoc on a File.
# @param file_name The file from which the lines are to be extracted.
# @param formats The pandoc output formats to be used, could be ("tex", "pdf").
# @param compile_latex Compile the LaTeX file?
def pandoc(file_name, compile_latex=False, formats="tex"):
    """
    Run Pandoc on a File
    """
    status = 1

    if is_tool("pandoc"):
        for form in formats:
            subprocess.call(["pandoc", "-sN", file_name, "-o",
                             modify_path(file_name=file_name, extension=form)])
        status = 0
        if compile_latex:
            status = 1
            tex_file_name = modify_path(file_name=file_name, extension="tex")
            if os.name == "posix":
                if is_tool("texi2pdf"):
                    subprocess.call(["texi2pdf", "--batch", "--clean",
                                     tex_file_name])
                    status = 0
            else:
                print("you are not running posix, see how to compile\n" +
                      tex_file_name +
                      "\nconsulting your operating system's documentation.")
    return status


#% main
if __name__ == "__main__":
    ##% parse command line arguments
    ARGS = make_parser().parse_args()
    ##% read markdown from file
    MARKDOWN_LINES = toc(file_name=ARGS.file_name,
                         comment_character=ARGS.comment_character,
                         magic_character=ARGS.magic_character)
    ##% get markdown file name
    MD_FILE_NAME = modify_path(file_name=ARGS.file_name,
                               postfix=ARGS.name_postfix,
                               prefix=ARGS.name_prefix,
                               extension="md")

    ## the file handler of markdown output
    MD_FILE = open(MD_FILE_NAME, "w")
    MD_FILE.writelines(MARKDOWN_LINES)
    MD_FILE.close()
    if ARGS.run_pandoc:
        pandoc(file_name=MD_FILE_NAME, compile_latex=ARGS.compile_latex,
               ## doxygen misses that this is a function's argument.
               formats=[ARGS.pandoc_formats])
    sys.exit(0)

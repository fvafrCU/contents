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
"""

#% import modules
from __future__ import print_function
import re
import subprocess
import os


## Test if a Program is Installed
#
# Will raise an error if the programm is not found.
# @param name The name of the program to be tested for.
# @return True if the Program is installed.
def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name, "-h"], stdout=devnull,
                         stderr=devnull).communicate()
        devnull.close()
    except OSError:
        print("please install " + name)
        if name == "pandoc" and os.name != "posix":
            print("you may try\n" + 'install.packages("installr"); ' +
                  'library("installr"); install.pandoc()\n' + "in GNU R")
        raise
    return True


## Extract Matching Lines
#
# Extract all lines starting with a combination of comment_character and
# magic_character from a file.
# @param file_name The file from which the lines are to be extracted.
# @param comment_character The comment character of the files language ("#" for
# example.
# @param magic_character The magic character marking lines as markdown
#  comments.
# @return A list of strings containing the lines extracted.
def extract_md(file_name, comment_character, magic_character):
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
# @return A list of strings containing the lines converted.
def convert(lines, comment_character, magic_character):
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
# @return A list of strings containing the lines extracted and converted.
def get_toc(file_name, comment_character, magic_character):
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
# @return A string containing the modified path.
def modify_path(file_name, postfix="", prefix="", extension=None):
    if extension is None:
        extension = os.path.splitext(file_name)[1]
    base_name = os.path.basename(os.path.splitext(file_name)[0])
    ext_base_name = prefix + base_name + postfix
    ext = extension.lstrip(".")
    name = os.path.join(os.path.dirname(file_name), ext_base_name) + "." + ext
    return name


## Run Pandoc on a File
#
# @param file_name The file from which the lines are to be extracted.
# @param formats The pandoc output formats to be used.
# @param compile_latex Compile the LaTeX file?
# @return True if parsing was successful.
def pandoc(file_name, compile_latex=False, formats="tex"):
    status = 1
    if is_tool("pandoc"):
        for form in formats.split(","):
            subprocess.call(["pandoc", "-sN", file_name, "-o",
                             modify_path(file_name=file_name, extension=form)])
            if compile_latex & (form == "tex"):
                tex_file_name = modify_path(file_name=file_name,
                                            extension="tex")
                if os.name == "posix":
                    if is_tool("texi2pdf"):
                        subprocess.call(["texi2pdf", "--batch", "--clean",
                                         tex_file_name])
                else:
                    print("you are not running posix, see how to compile\n" +
                          tex_file_name +
                          "\nconsulting your operating system's " +
                          "documentation.")
    status = 0
    return status


## Extract, Convert and Save Markdown Style Comments From a File
#
# This is merely a wrapper to get_toc(), modify_path() and pandoc().
# @param file_name The file from which the lines are to be extracted.
# @param pandoc_formats The pandoc output formats to be used.
# @param run_pandoc Run pandoc on the markdown file created?
# @param compile_latex Compile the LaTeX file?
# @param postfix Set the content's file postfix.
# @param prefix Set the content's file prefix.
# @param comment_character The comment character of the files language ("#" for
# example.
# @param magic_character The magic character marking lines as markdown
#  comments.
# @return True if content generation was successful.
def contents(file_name, comment_character="#", magic_character="%",
             prefix="", postfix="", run_pandoc=True,
             compile_latex=False, pandoc_formats="tex"):
    status = 1
    ##% read markdown from file
    markdown_lines = get_toc(file_name=file_name,
                             comment_character=comment_character,
                             magic_character=magic_character)
    ##% get markdown file name
    md_file_name = modify_path(file_name=file_name,
                               postfix=postfix,
                               prefix=prefix,
                               extension="md")
    ## the file handler of markdown output
    md_file = open(md_file_name, "w")
    md_file.writelines(markdown_lines)
    md_file.close()
    status = 0
    if run_pandoc:
        status = pandoc(file_name=md_file_name, compile_latex=compile_latex,
                        ## doxygen misses that this is a function's argument.
                        formats=pandoc_formats)
    return status

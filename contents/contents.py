#!/usr/bin/env python3
## @file 
#  module functions

#######% % markdown comments for various source files
#######% % Dominik Cullmann
#######%
#######% extract markdown-like comments from (source code) file, convert them
#######% to valid markdown and run pandoc on it.
#######% Since the comment characters for different languages differ,
#######% this program can be adjusted to use the comment character used in your
#######% file by command line arguments.
#######%

#% import modules
from __future__ import print_function
import re


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



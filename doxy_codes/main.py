#!/usr/bin/env python3
# @file
# module functions
#


#% import modules
from __future__ import print_function
import re
import os



## @brief     Extract Matching Lines
#
#    Extract all lines starting with a combination of comment_character and
#    magic_character from a file.
#
#
# @param		file_name	The file from which the lines are to be extracted.
# @param		comment_character	The comment character of the files language.
# @param		magic_character	The magic character marking lines as excerpts.
# @return
#         A list of strings containing the lines extracted.
#

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


## @brief     Convert Lines to Markdown
#
#    Remove whitespace and magic characters from lines and output valid markdown.
#
# @param		lines	The lines to be converted.
# @param		comment_character	The comment character of the files language.
# @param		magic_character	The magic character marking lines as excerpts.
# @return
#        A list of strings containing the lines converted.
#

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


## @brief     Get Table of Contents
#
#    Just a wrapper to extract_md() and convert().
#
#
# @param		file_name	The file from which the lines are to be extracted.
# @param		comment_character	The comment character of the files language.
# @param		magic_character	The magic character marking lines as excerpts.
# @return
#        A list of strings containing the lines extracted and converted.
#

def get_toc(file_name, comment_character, magic_character):
    lines_matched = extract_md(file_name=file_name,
                               comment_character=comment_character,
                               magic_character=magic_character)
    converted_lines = convert(lines=lines_matched,
                              comment_character=comment_character,
                              magic_character=magic_character)
    return converted_lines


## @brief     Modify a Path
#
#    Add a postfix and a prefix to the basename of a path and optionally change
#    it's extension.
#
# @param		file_name	The file to be modified.
# @param		postfix	Set the output file postfix.
# @param		prefix	Set the output file prefix.
# @param		extension	Set a new file extension.
# @param		output_path	Set a new file name or an output directory.
# @return
#        A string containing the modified path.
#

def modify_path(file_name, postfix="", prefix="", output_path="",
                extension=None):
    if output_path != "" and not os.path.isdir(output_path):
        name = output_path
    else:
        base_name = os.path.basename(os.path.splitext(file_name)[0])
        ext_base_name = prefix + base_name + postfix
        if extension is None:
            extension = os.path.splitext(file_name)[1]
        ext = extension.lstrip(".")
        if output_path == "":
            directory = os.path.dirname(file_name)
        else:
            directory = output_path
        name = os.path.join(directory, ext_base_name) + "." + ext
    return name

#!/usr/bin/env python3
# @file
# user interface functions
#

from . import main
from . import op


## @brief     Extract, Convert and Save Markdown Style Comments From a File
#
#    This is merely a wrapper to get_toc(), modify_path() and pandoc().
#
#
# @param		file_name	The file from which the lines are to be extracted.
# @param		pandoc_formats	The pandoc output formats to be used.
# @param		run_pandoc	Run pandoc on the markdown file created?
# @param		compile_latex	Compile the LaTeX file?
# @param		postfix	Set the output file postfix.
# @param		prefix	Set the output file prefix.
# @param		comment_character	The comment character of the files language.
# @param		output_path	Set a new file name or an output directory.
# @param		magic_character	The magic character marking lines as excerpts.
# @return
#        0 if output generation was successful.
#

def excerpt(file_name, comment_character="#", magic_character="%",
            output_path="",
            prefix="", postfix="", run_pandoc=True,
            compile_latex=False, pandoc_formats="tex"):
    status = 1
    ##% read markdown from file
    markdown_lines = main.get_toc(file_name=file_name,
                                  comment_character=comment_character,
                                  magic_character=magic_character)
    ##% get markdown file name
    md_file_name = main.modify_path(file_name=file_name,
                                    output_path=output_path,
                                    postfix=postfix,
                                    prefix=prefix,
                                    extension="md")
    ## the file handler of markdown output
    md_file = open(md_file_name, "w")
    md_file.writelines(markdown_lines)
    md_file.close()
    status = 0
    if run_pandoc:
        status = op.pandoc(file_name=md_file_name,
                           ## doxygen misses: this is a function's argument.
                           compile_latex=compile_latex,
                           ## doxygen misses: this is a function's argument.
                           formats=pandoc_formats)
    return status

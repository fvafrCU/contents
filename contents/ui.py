#!/usr/bin/env python3
## @file 
#  user interface functions

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



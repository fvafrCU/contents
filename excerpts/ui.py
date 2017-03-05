#!/usr/bin/env python3
"""
 @file
 user interface functions
"""
from . import main
from . import op


def excerpts(file_name, comment_character="#", magic_character="%",
             output_path="",
             prefix="", postfix="", run_pandoc=True,
             compile_latex=False, pandoc_formats="tex"):
    """
    Extract, Convert and Save Markdown Style Comments From a File

    This is merely a wrapper to excerpt(), modify_path() and pandoc().

    Kwargs:
        file_name: The file from which the lines are to be extracted.
        pandoc_formats: The pandoc output formats to be used.
        run_pandoc: Run pandoc on the markdown file created?
        compile_latex: Compile the LaTeX file?
        postfix: Set the output file postfix.
        prefix: Set the output file prefix.
        comment_character: The comment character of the files language.
        output_path: Set a new file name or an output directory.
        magic_character: The magic character marking lines as excerpts.
    Returns:
        0 if output generation was successful.
    """
    status = 1
    markdown_lines = main.excerpt(file_name=file_name,
                                  comment_character=comment_character,
                                  magic_character=magic_character)
    md_file_name = main.modify_path(file_name=file_name,
                                    output_path=output_path,
                                    postfix=postfix,
                                    prefix=prefix,
                                    extension="md")
    md_file = open(md_file_name, "w")
    md_file.writelines(markdown_lines)
    md_file.close()
    status = 0
    if run_pandoc:
        status = op.pandoc(file_name=md_file_name,
                           # doxygen misses: this is a function's argument.
                           compile_latex=compile_latex,
                           # doxygen misses: this is a function's argument.
                           formats=pandoc_formats)
    return status

#!/usr/bin/env python3
import excerpts
import shutil 
source = "tests/files/some_file.txt"
sink = "output/some_file.txt"
shutil.copyfile(source, sink)
print(excerpts.excerpt(file_name=sink, 
                       comment_character='#', 
                       magic_character='%',
                       pandoc_formats="html,tex", 
                       compile_latex=True))
print(excerpts.excerpt(file_name = sink, 
                       comment_character='#', 
                       magic_character='%',
                       prefix="standard_"))
print(excerpts.get_toc(file_name = sink, 
                       comment_character='#', 
                       magic_character='%'))

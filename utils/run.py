#!/usr/bin/env python3
import excerpts
import shutil 
import os
source = "tests/files/some_file.txt"
sink = './output/some_file.txt'
dir = os.path.dirname(sink)
if not os.path.exists(dir):
    os.makedirs(dir)
shutil.copyfile(source, sink)
print(excerpts.excerpts(file_name=sink, 
                       comment_character='#', 
                       magic_character='%',
                       pandoc_formats="html,tex", 
                       compile_latex=True))
print(excerpts.excerpts(file_name = sink, 
                       comment_character='#', 
                       magic_character='%',
                       prefix="standard_"))
print(excerpts.excerpt(file_name = sink, 
                       comment_character='#', 
                       magic_character='%'))

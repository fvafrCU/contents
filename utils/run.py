#!/usr/bin/env python3
import contents
import shutil 
source = "tests/files/some_file.txt"
sink = "output/some_file.txt"
shutil.copyfile(source, sink)
print(contents.contents(file_name=sink, 
                       comment_character='#', 
                       magic_character='%',
                       pandoc_formats="html,tex", 
                       compile_latex=True))
print(contents.contents(file_name = sink, 
                       comment_character='#', 
                       magic_character='%',
                       prefix="standard_"))
print(contents.get_toc(file_name = sink, 
                       comment_character='#', 
                       magic_character='%'))

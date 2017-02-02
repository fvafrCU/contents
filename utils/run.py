#!/usr/bin/env python3
import contents
import shutil 
source = "contents/contents.py"
sink = "output/contents.py"
shutil.copyfile(source, sink)
print(contents.contents(file_name=sink, 
                       comment_character='#', 
                       magic_character='%',
                       pandoc_formats="html,tex", 
                       compile_latex=True))
print(contents.contents(file_name = sink, 
                       comment_character='#', 
                       magic_character='%',
                       prefix="standard"))
print(contents.get_toc(file_name=sink, 
                       comment_character='#', 
                       magic_character='%'))

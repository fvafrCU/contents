#!/usr/bin/env python3
import contents
print(contents.get_toc(file_name = "contents/contents.py", 
                       comment_character = '#', 
                       magic_character = '%'))
print(contents.contents(file_name = "contents/contents.py", 
                       comment_character = '#', 
                       magic_character = '%'))

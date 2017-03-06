# -*- coding: utf-8 -*-

from context import excerpts

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_excerpt(self): 
        result = excerpts.excerpt(file_name="tests/files/some_file.txt", 
                                  comment_character='#', 
                                  magic_character='%')
        expectation =  ['% All About Me\n', '% Me\n', 
        '**This** is an example of a markdown paragraph: markdown recognizes\n',
        'only six levels of heading, so we use seven or more levels to mark\n', 
        '"normal" text.\n', 
        'Here you can use the full\n', 
        '[markdown syntax](http://daringfireball.net/projects/markdown/syntax).\n', 
        '*Note* the trailing line: markdown needs an empty line to end a\n', 
        'paragraph.\n', '\n', '# A section\n', '## A subsection\n', 
        'Another markdown paragraph.\n', '\n']
        self.assertEqual(expectation, result)


    def test_excerpt_nopep(self): 
        result = excerpts.excerpt(file_name="tests/files/some_file.txt", 
                                  comment_character='#', 
                                  magic_character='%',
                                  allow_pep8=False)
        expectation =  ['% All About Me\n', '% Me\n', 
        '**This** is an example of a markdown paragraph: markdown recognizes\n',
        'only six levels of heading, so we use seven or more levels to mark\n', 
        '"normal" text.\n', 
        'Here you can use the full\n', 
        '[markdown syntax](http://daringfireball.net/projects/markdown/syntax).\n', 
        '*Note* the trailing line: markdown needs an empty line to end a\n', 
        'paragraph.\n', '\n', '# A section\n', '## A subsection\n', 
        'Another markdown paragraph.\n', '\n']
        self.assertEqual(expectation, result)


    def test_excerpts(self): 
        excerpts.excerpts(file_name="tests/files/some_file.txt", 
                          comment_character='#', 
                          magic_character='%')
        with open("tests/files/some_file.md") as f:
            result = f.readlines() 
        f.close()
        expectation =  ['% All About Me\n', '% Me\n', 
        '**This** is an example of a markdown paragraph: markdown recognizes\n',
        'only six levels of heading, so we use seven or more levels to mark\n', 
        '"normal" text.\n', 
        'Here you can use the full\n', 
        '[markdown syntax](http://daringfireball.net/projects/markdown/syntax).\n', 
        '*Note* the trailing line: markdown needs an empty line to end a\n', 
        'paragraph.\n', '\n', '# A section\n', '## A subsection\n', 
        'Another markdown paragraph.\n', '\n']
        self.assertEqual(expectation, result)


class PathModificationSuite(unittest.TestCase):
    """path modification test cases."""


    def test_output_file_name(self): 
        result = excerpts.main.modify_path(file_name="files/some_file.txt", 
                                  output_path='/tmp/foo.txt')
        expectation = "/tmp/foo.txt"
        self.assertEqual(expectation, result)


    def test_output_dir(self): 
        result = excerpts.main.modify_path(file_name="files/some_file.txt", 
                                  output_path='/tmp/')
        expectation = "/tmp/some_file.txt"
        self.assertEqual(expectation, result)


    def test_no_output(self): 
        result = excerpts.main.modify_path(file_name="files/some_file.txt",
                extension="bar", postfix="_post", prefix="pre_")
        expectation = "files/pre_some_file_post.bar"
        self.assertEqual(expectation, result)


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-

from context import excerpts

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_get_toc(self): 
        result = excerpts.get_toc(file_name="tests/files/some_file.txt", 
                                  comment_character='#', 
                                  magic_character='%')
        expectation =  ['% All About Me\n', '% Me\n', 
        '**This** is an example of a markdown paragraph: markdown recognizes\n',
        'only six levels of heading, so we use seven or more levels to mark\n', 
        '"normal" text.\n', 
        'Here you can use the full\n', 
        '[markdown syntax](http://daringfireball.net/projects/markdown/syntax).\n', 
        '*Note* the trailing line: markdown needs an empty line to end a\n', 
        'paragraph.\n', '\n', '# A section\n', '# A subsection\n', 
        'Another markdown paragraph.\n', '\n']
        self.assertEqual(expectation, result)

    def test_excerpts(self): 
        excerpts.excerpt(file_name="tests/files/some_file.txt", 
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
        'paragraph.\n', '\n', '# A section\n', '# A subsection\n', 
        'Another markdown paragraph.\n', '\n']
        self.assertEqual(expectation, result)

if __name__ == '__main__':
    unittest.main()

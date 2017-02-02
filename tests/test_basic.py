# -*- coding: utf-8 -*-

from context import contents

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_get_toc(self): 
        result = contents.get_toc(file_name="tests/files/some_file.py", 
                                  comment_character='#', 
                                  magic_character='%')
        expectation = ['% markdown comments for various source files\n', 
                '% Dominik Cullmann\n', '\n', 
                'extract markdown-like comments from (source code) file, convert them\n', 
                'to valid markdown and run pandoc on it.\n', 
                'Since the comment characters for different languages differ,\n', 
                'this program can be adjusted to use the comment character used in your\n', 
                'file by command line arguments.\n', '\n', 
                '# import modules\n', '## read markdown from file\n', 
                '## get markdown file name\n']
        self.assertEqual(expectation, result)


if __name__ == '__main__':
    unittest.main()

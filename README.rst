Excerpts
========

Exract markdown style comments from a file.

Ever read or wrote source files containing sectioning comments?
If these comments are markdown style section comments, we can extract them and
set a table of contents.

Suppose you have a file reading:

.. code:: python

    file_name = 'tests/files/some_file.txt'
    with open(file_name, 'r') as fin:
        print(fin.read())
    

.. code::

    #######% % All About Me
    #######% % Me
    ####### The above defines a pandoc markdown header.
    ####### This is more text that will not be extracted.
    #######% **This** is an example of a markdown paragraph: markdown
    #######% recognizes only six levels of heading, so we use seven or
    #######% more levels to mark "normal" text.
    #######% Here you can use the full markdown
    #######% [syntax](http://daringfireball.net/projects/markdown/syntax).
    #######% *Note* the trailing line: markdown needs an empty line to end
    #######% a paragraph.
    #######%
    
    #% A section
    ##% A subsection
    ### Not a subsubsection but a plain comment.
    ############% Another markdown paragraph.
    ############%
    ####### More text that will not be extracted.
    
    
    



Then excperting the marked comments

.. code:: python

    import excerpts
    with open(file_name) as infile:
        lines = infile.readlines()
    
    excerpted = excerpts.excerpt(lines = lines, comment_character="#",
        magic_character="%")
    print(*excerpted)
    

.. code::

    % All About Me
     % Me
     **This** is an example of a markdown paragraph: markdown
     recognizes only six levels of heading, so we use seven or
     more levels to mark "normal" text.
     Here you can use the full markdown
     [syntax](http://daringfireball.net/projects/markdown/syntax).
     *Note* the trailing line: markdown needs an empty line to end
     a paragraph.
    
     # A section
     ## A subsection
     Another markdown paragraph.
    
    
    
    





Requirements
------------

Excerpts needs python3.

Installation
------------
Try 
  pip3 install git+git://github.com/fvafrcu/excerpts --upgrade --user

  

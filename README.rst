Excerpts
========

Introduction
------------
Excerpt markdown style comments from a file.

Ever read or wrote source files containing sectioning comments?
If these comments are markdown style section comments, we can extract them and
set a table of contents.

By Example
----------
Suppose you have a file reading:

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
    
    
    



Then excerpting the marked comments via

.. code:: python

    import excerpts
    with open(file_name) as infile:
        lines = infile.readlines()
    
    excerpted = excerpts.excerpt(lines = lines, comment_character="#",
        magic_character="%")
    




.. code:: python

    print (''.join(str(p) for p in excerpted))
    


gives

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
    
    
    
    


which is valid 
`markdown <https://daringfireball.net/projects/markdown/>`_
for 
`pandoc <https://www.pandoc.org>`_
.

Working with Files
~~~~~~~~~~~~~~~~~~
If you want to excerpt from a file and run pandoc on the result, you can use


.. code:: python

    excerpts.excerpts(file_name = file_name, comment_character="#",
        magic_character="%", output_path="output", run_pandoc=True,
        pandoc_formats="html")
    


to generate 
`this file. <output/some_file.html>`_
Excerpts ships with a command line interface that you may call from your
operating systems' command line instead of from python3:

.. code::

    usage: excerpts [-h] [-O OUTPUT_PATH] [-o POSTFIX] [-e PREFIX]
                    [-c COMMENT_CHARACTER] [-m MAGIC_CHARACTER] [-v] [-x]
    [-p]
                    [-n] [-l] [--no-latex] [--formats PANDOC_FORMATS]
    [--no-pep8]
    
    
    



PEP8 
----
PEP8 requires each "line of a block comment starts with a # and a single space".
excerpts takes care of this requirement by removing a single comment character
that is followed by a space and a sequence of comments characters.
Should you need to disable this behaviour, you can set allow_pep8 to False.


Requirements
------------

Excerpts needs python3.

Installation
------------
Try 
  pip3 install git+git://github.com/fvafrcu/excerpts --upgrade --user

  

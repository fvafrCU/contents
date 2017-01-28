% markdown comments for various source files
% Dominik Cullmann

extract markdown-like comments from (source code) file, convert them
to valid markdown and run pandoc on it.
Since the comment characters for different languages differ,
this program can be adjusted to use the comment character used in your
file by command line arguments.

copyright: 2014-2017, Dominik Cullmann
license: BSD 2-Clause
maintainer: Dominik cullmann
email: dominik.cullmann@forst.bwl.de

# import modules
## *This* is an example markdown comment of heading level 2
**This** is an example of a markdown paragraph: markdown recognizes
only six levels of heading, so we use seven levels to mark
"normal" text.
Here you can use the full
[markdown syntax](http://daringfireball.net/projects/markdown/syntax).
*Note* the trailing line: markdown needs an empty line to end a
paragraph.

# main
## parse command line arguments
## read markdown from file
## get markdown file name

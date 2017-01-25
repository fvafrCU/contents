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

# define parser
# define converter
remove 7 or more heading levels.  
remove the first occurence of the magic_character
(the header definition of pandoc"s markdown uses the
percent sign, if that is the magic pattern, all pandoc
standard headers would end up to be simple text.  
empty lines (ending markdown paragraphs) are not written by
file.write(), so we replace them by newlines.

# write file contents
## get matchting lines
## convert matched lines to markdown
## write md file
## run pandoc
### If on posix...
#### ... tex it
#### ... warn otherwise
# main
## parse command line arguments

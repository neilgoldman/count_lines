line_counter
============

Simple Python script to count lines of code and comments in a project.

Tested with Python 2.7.8, but should work with Python 3 as well.

Make sure to open the file and customize the file extensions and sequences to use for comments/block-comments. The project directory to scan can be set inside of the script, or passed as a commandline argument. If no directory is provided, it will scan the current working directory.

In some cases it may not always be 100% accurate, but lines-of-code is a crappy (but fun!) metric anyways. The printed numbers may not add up to the printed total, because the printed total doesn't count any blank lines at the end of the file, but blank_lines does.
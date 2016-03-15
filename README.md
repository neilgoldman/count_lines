line_counter
============

Simple Python script to count lines of code and comments in a project.

Usage Examples:

    $ python count_lines.py
    Breakdown by language:
		Python
        144 lines total
        103 lines of code (71.5%)
        19 lines of comments (13.2%)
        22 lines of whitespace (15.3%)

    $ python count_lines.py /c/Path/To/Your/Project

Tested with Python 2.7 and Python 3.5 on Windows. There doesn't seem to be anything that would break it on Unix/Linux/OSX, but I have not tested it.

Make sure to open the file and customize the file extensions and sequences to use for comments/block-comments. The current defaults are for a project using Python, C#, HTML/CSS/JS. The project directory to scan can be set inside of the script, or passed as a commandline argument. If no directory is provided, it will scan the current working directory.

In some cases it may not always be 100% accurate, but lines-of-code is a crappy (but fun!) metric anyways.

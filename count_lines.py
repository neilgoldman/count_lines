__author__ = "Neil Goldman"

import os
import sys

'''
Change the following vars to match your project, the example
setup below is for a project using mixed python and C# files

directory can have it's value set here, or passed as a commandline argument
'''

directory = r''  # r'A:\bsolute\Path\To\FilesDirectory'
verbose_output = False  # Prints all files counted
language_extensions = ['.py', '.cs']
ignore_files = ['']  # Place name of file and extension here. Not full path
ignore_dirs = ['.idea', '.git']  # Directories to be ignored

# Append any single-line comment sequences in any order
single_line_comments = ['#', '//']
# Add tuples containing block-comment opening and closing sequences
block_comments = [('/*', '*/'), ("'''", "'''")]


def count_lines(directory):
    if len(sys.argv) > 1:
        directory = sys.argv[1]

    if not directory:
        directory = os.getcwd()

    print('opening ' + directory + '\n')
    code_lines = 0
    blank_lines = 0
    comment_lines = 0
    total_lines = 0

    for root, subfolders, files in os.walk(directory, topdown=True):
        subfolders[:] = [d for d in subfolders if d not in ignore_dirs]

        for f in files:
            name, extension = os.path.splitext(f)
            if f in ignore_files or extension not in language_extensions:
                continue
            if verbose_output:
                print('file: ' + f)

            filename = os.path.join(root, f)
            file_obj = open(filename, 'r')

            in_block_comment = False
            for line in file_obj:
                line = line.strip()

                # Check if we're in a block comment
                if in_block_comment:
                    comment_lines += 1
                    in_block_comment = check_block_comment(line, in_block_comment)
                # Check for blank lines
                elif not line:
                    blank_lines += 1
                # Check if a block comment is at the start of the line
                elif any(line.startswith(seq[0]) for seq in block_comments):
                    comment_lines += 1
                    in_block_comment = check_block_comment(line, in_block_comment)
                # Check for block comments after some valid code (eww)
                elif any(seq[0] in line for seq in block_comments):
                    code_lines += 1
                    in_block_comment = check_block_comment(line, in_block_comment)
                # Check for single line comment with no code
                elif any(line.startswith(seq[0]) for seq in single_line_comments):
                    comment_lines += 1
                else:
                    code_lines += 1

    print(str(code_lines) + ' lines of code counted.')
    print(str(blank_lines) + ' blank lines counted.')
    print(str(comment_lines) + ' lines of comments counted.')


# Tests whether the current line ends a block comment
# A line can both open and close a block comment, or just close one
# Simple approach, won't catch cases where a block-comment ends and
# then starts a new block-comment on the same line, but who even does that?
def check_block_comment(line, in_block_comment):
    for seq in block_comments:
        if seq[0] == seq[1]:
            num_comment_seq = line.count(seq[0])
            if num_comment_seq and num_comment_seq % 2 == 0:
                return False
        if seq[1] in line and in_block_comment:
            return False
    return True


count_lines(directory)

__author__ = "Neil Goldman"

import os
import sys
import io

'''
Change the following vars to match your project, the example
setup below is for a project using mixed python and C# files

directory can have it's value set here, or passed as a commandline argument
'''

directory = r''  # r'A:\bsolute\Path\To\FilesDirectory'
verbose_output = False  # Prints all files counted
language_extensions = ['.py', '.cs', '.js', '.css', '.html']
ignore_files = ['']  # Place name of file and extension here. Not full path
ignore_dirs = ['.idea', '.git', 'node_modules', 'bower_components']  # Directories to be ignored

language_map = {
    '.py': 'Python',
    '.cs': 'C#',
    '.js': 'JavaScript',
    '.css': 'CSS',
    '.html': 'HTML',
}
language_count_map = {v:{'total': 0, 'code': 0, 'comments': 0, 'whitespace': 0} for k,v in language_map.items()}

# Append any single-line comment sequences in any order
single_line_comments = ['#', '//']
# Add tuples containing block-comment opening and closing sequences
block_comments = [('/*', '*/'), ("'''", "'''"), ('"""', '"""'), ('<!--', '-->')]


def count_lines(directory):
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        # Sometimes (on windows at least), using a single backslash at the end of a quoted directory name will include the quote
        # e.g. thecount_lines.py "C:\my_projects\src\",sys.argv[1] will be equal to `C:\my_projects\src"`
        if directory.endswith('"') or directory.endswith('"'):
            directory = directory[:-1]

    if not directory:
        directory = os.getcwd()

    print('opening ' + directory + '\n')
    code_lines = 0
    blank_lines = 0
    comment_lines = 0
    total_lines = 0

    for root, dirnames, files in os.walk(directory, topdown=True):
        # Filter any directories in the ignore_dirs before calling os.walk
        # You can modify dirnames in-place and os.walk will use that modified list in the walk (when topdown=True).
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for f in files:
            name, extension = os.path.splitext(f)
            if f in ignore_files or extension not in language_extensions:
                continue
            if verbose_output:
                print('file: ' + os.path.join(root, f))
            current_lang = language_map[extension]

            filename = os.path.join(root, f)
            file_obj = io.open(filename, 'r', encoding='utf-8')

            in_block_comment = False
            # Keep a running count of the counted lines, but don't add them to total
            # until we're sure this isn't file-trailing whitespace
            # Same thing with whitespace count. We don't want to count trailing whitespace unless it has valid code/comments after
            # Technically we can do tmp_whitespace_counter = lines_counted-1 at the end of the loop, but this is easier to reason about.
            lines_counted = 0
            tmp_whitespace_counter = 0

            for line in file_obj:
                lines_counted += 1
                end_of_code = True  # Are we at the end of code-content? (not actual eof)
                line = line.strip()

                # Check if we're in a block comment
                if in_block_comment:
                    end_of_code = False
                    comment_lines += 1
                    language_count_map[current_lang]['comments'] += 1
                    in_block_comment = check_block_comment(line, in_block_comment)
                # Check for blank lines
                elif not line:
                    tmp_whitespace_counter += 1
                # Check if a block comment is at the start of the line
                elif any(line.startswith(seq[0]) for seq in block_comments):
                    end_of_code = False
                    comment_lines += 1
                    language_count_map[current_lang]['comments'] += 1
                    in_block_comment = check_block_comment(line, in_block_comment)
                # Check for block comments after some valid code (eww)
                elif any(seq[0] in line for seq in block_comments):
                    end_of_code = False
                    code_lines += 1
                    language_count_map[current_lang]['code'] += 1
                    in_block_comment = check_block_comment(line, in_block_comment)
                # Check for single line comment with no code
                elif any(line.startswith(seq[0]) for seq in single_line_comments):
                    end_of_code = False
                    comment_lines += 1
                    language_count_map[current_lang]['comments'] += 1
                else:
                    end_of_code = False
                    code_lines += 1
                    language_count_map[current_lang]['code'] += 1

                if not end_of_code: # We just read a non-whitespace line, so total things up
                    blank_lines += tmp_whitespace_counter
                    language_count_map[current_lang]['whitespace'] += tmp_whitespace_counter

                    language_count_map[current_lang]['total'] += lines_counted
                    total_lines += lines_counted

                    tmp_whitespace_counter = 0
                    lines_counted = 0
                # else: we may be at the end of the code, but reading 100 empty lines at the end of the file, don't count that.

            file_obj.close()

    print(str(code_lines) + ' lines of code counted.')
    print(str(blank_lines) + ' blank lines counted.')
    print(str(comment_lines) + ' lines of comments counted.')
    print(str(total_lines) + ' total lines counted.')
    print()
    print('Breakdown by language:')
    for lang_name in language_count_map.keys():
        if language_count_map[lang_name]['total'] == 0:
            continue
        print(lang_name)
        for line_type in ['total', 'code', 'comments', 'whitespace']:
            if line_type == 'total':
                print('\t{} lines {}'.format(language_count_map[lang_name][line_type], line_type))
            else:
                percent = language_count_map[lang_name][line_type] / language_count_map[lang_name]['total']
                percent = percent * 100.0
                print('\t{} lines of {} ({:.1f}%)'.format(language_count_map[lang_name][line_type], line_type, percent))


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

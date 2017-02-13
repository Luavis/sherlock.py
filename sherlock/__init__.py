"""Sherlock: Python to bash transcompiler

"""
import stat
import argparse
import tempfile
from os import path, system, chmod
from sherlock.codelib.analyzer import CodeAnalyzer


__author__ = "Luavis Kang"
__copyright__ = "Copyright 2017, Luavis"
__credits__ = ["Luavis Kang", ]
__license__ = "MIT"
__version__ = "0.2.0"
__status__ = "Development"

__maintainer__ = "Luavis Kang"
__email__ = "luaviskang@gmail.com"


parser = argparse.ArgumentParser(description='Python to bash trans-compiler.')
parser.add_argument('input', metavar='[file | command]', type=str, help='program read from script file ')
parser.add_argument('-o', dest='output', metavar='output', type=str, help='output file path')
parser.add_argument('-c', '--command', dest='is_command', action='store_true', default=False, help='program passed in as string')
parser.add_argument('-v', '--verbose', dest='is_verbose', action='store_true', default=False, help='program run in verbose mode')
parser.add_argument('--version', action='version', version='Sherlock %s' % __version__)


def print_error(msg):
    print('sherlock: %s' % msg)

def save_code(path, code):
    with open(path, 'w') as f:
        f.write("#!/usr/bin/env bash\n")
        f.write(code)
    chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

def compile_script(script):
    analyzer = CodeAnalyzer(script)
    generator = analyzer.analysis()
    return generator.generate()

def execute_from_command_line():
    args = parser.parse_args()

    try:
        script = ''
        if args.is_command:
            script = args.input
        elif path.isfile(args.input):
            with open(args.input) as f:
                script = f.read()
        else:
            print_error("can't open file '%s'" % args.input)

        code = compile_script(script)
        if args.is_verbose:
            print(code)
        if args.output is None:
            tf = tempfile.NamedTemporaryFile()
            name = tf.name
            save_code(name, code)
            # print('cat %s | bash' % name)
            system('sh -c "$(cat %s)"' % name)
        else:
            save_code(args.output, code)
    except IOError:
        import sys
        e = sys.exc_info()[1]
        print_error("can't open file: %s" % (e))


if __name__ == '__main__':
    execute_from_command_line()

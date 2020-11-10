import inspect
import argparse
import re
import sys

import rapidenv

__MODULES_IGNORE_LIST__ = ['helpers']


def vdir(obj):
    return [x for x in dir(obj) if not x.startswith('__') and x != obj.__name__.split('.')[-1]
            and x not in __MODULES_IGNORE_LIST__]


def main():
    argv = sys.argv[1:]  # ['path', 'copy_path', "-h"] # "--args='c:/temp/a.txt', 'c:/temp/test/a.txt'"]

    # iteration variables
    module = rapidenv
    prog = 'rapidenv'
    args = None

    # define main menu parser
    parser = argparse.ArgumentParser(prog=prog, description=f'{prog} v{rapidenv.__version__}, '
                                                            f'an environment helpers utility.',
                                     add_help=False)
    entries = vdir(module)
    parser.add_argument('opt', type=str, choices=entries)
    parser.add_argument('-h', '--help', action='store_true', help='show this help menu and exit.')

    # print help if no arguments and exit
    if len(argv) == 0:
        # main menu
        parser.print_help()
        return 0

    # iterate modules
    for i in range(1000):  # limit iteration number for endless loop protection
        # update iteration parameters
        args = parser.parse_known_args(argv)[0]  # accept unrecognized args
        obj = getattr(module, args.opt)
        argv = argv[1:]

        # exit condition
        if not inspect.ismodule(obj):
            break

        # update module
        module = obj
        prog += ' ' + args.opt

        # iteration step
        # todo add module description if exists
        parser = argparse.ArgumentParser(prog=prog, description=f'{prog} helpers utilities.',
                                         add_help=False)
        entries = vdir(module)
        parser.add_argument('opt', type=str, choices=entries)
        parser.add_argument('-h', '--help', action='store_true', help='show this help menu and exit.')

        # if help is next arg, print help and exit
        if len(argv) > 0 and (argv[0] == "-h" or argv[0] == "--help"):
            parser.print_help()
            return 0
        else:
            args = parser.parse_known_args(argv)[0]

    # handle function
    obj = getattr(module, args.opt)
    prog += ' ' + args.opt
    if inspect.isfunction(obj):
        # build function docstring
        if obj.__doc__:
            docstr = "\n" + re.sub(r'\n[ ]+', '\n', obj.__doc__)
        else:
            docstr = ""

        # define parser
        parser = argparse.ArgumentParser(prog=prog, description=f'{prog} helpers utility. {docstr}',
                                         add_help=False, formatter_class= argparse.RawTextHelpFormatter)
        parser.add_argument('-h', '--help', action='store_true', help='show this help menu and exit.')
        parser.add_argument('-a', '--args', dest='fargs', type=str, action='store', help=f'{args.opt} arguments',
                            default='')
        if len(argv) > 0 and (argv[0] == "-h" or argv[0] == "--help"):
            parser.print_help()
            return 0

        args = parser.parse_known_args(argv)[0]

        tprog = prog.replace(' ', '.')
        try:
            eval(f"{tprog}({args.fargs})")
        except Exception as e:
            print(f"failed to execute {prog} with args: {args.fargs}")
            print(f"Error: {e}")
            return 1
    else:
        # should never get here
        print(f"'{args.opt}' is not supported.")

    print('here')


if __name__ == "__main__":
    exit(main())

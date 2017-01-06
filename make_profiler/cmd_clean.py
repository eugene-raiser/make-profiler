#!/usr/bin/python3

import os
import sys
import logging
import shutil
import argparse

from make_profiler.parser import parse, get_dependencies_influences, Tokens


def rm_node(node):
    if not os.path.exists(node):
        return
    logging.info('removing %s', node)
    if os.path.isdir(node):
        shutil.rmtree(node)
    else:
        os.remove(node)


def clean_target(t, deps):
    if t not in deps:
        return
    for sub_t in deps[t]:
        rm_node(sub_t)
        clean_target(sub_t, deps)


def main(argv=sys.argv[1:]):
    options = argparse.ArgumentParser(
        description='Removes the target and everything this target leads to.')
    options.add_argument(
        '-f',
        action='store',
        dest='in_filename',
        type=str,
        default='Makefile',
        help='Makefile to read (default %(default)s)')
    options.add_argument(
        'targets',
        default=['all'],
        metavar='target',
        type=str,
        nargs='*',
        help='Targets to process')

    args = options.parse_args(argv)
    in_file = open(args.in_filename, 'r') if args.in_filename else sys.stdin

    ast = parse(in_file)
    deps, influences, order_only, indirect_influences = get_dependencies_influences(ast)

    for target in args.targets:
        clean_target(influences, target)


if __name__ == '__main__':
    main()

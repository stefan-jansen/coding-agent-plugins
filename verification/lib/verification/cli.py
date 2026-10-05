"""Command dispatch. Every gate is a subcommand that exits non-zero on failure."""

import argparse
import os
import sys

from . import store


def _store_or_absent():
    path = store.location()
    if path is None:
        print("store absent")
    return path


def cmd_store_check(_args):
    path = _store_or_absent()
    if path is None:
        return 0
    problems = store.check(path)
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(f"store check: {len(problems)} problem(s) in {path}", file=sys.stderr)
        return 1
    print(f"store check: ok ({path})")
    return 0


def cmd_store_index(_args):
    path = _store_or_absent()
    if path is None:
        return 0
    with open(os.path.join(path, store.INDEX_FILE), "w", encoding="utf-8") as fh:
        fh.write(store.render_index(path))
    print(f"wrote {store.INDEX_FILE}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="verification")
    groups = parser.add_subparsers(dest="group", required=True)
    st = groups.add_parser("store", help="the private store of entries and corpus")
    st_cmds = st.add_subparsers(dest="command", required=True)
    st_cmds.add_parser("check", help="validate rows, sizes and pointers").set_defaults(
        func=cmd_store_check
    )
    st_cmds.add_parser("index", help="regenerate the loaded index").set_defaults(
        func=cmd_store_index
    )
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)

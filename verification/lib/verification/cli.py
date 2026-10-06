"""Command dispatch. Every gate is a subcommand that exits non-zero on failure."""

import argparse
import os
import sys

from . import classify, corpus, store


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


def cmd_corpus_report(_args):
    path = _store_or_absent()
    if path is None:
        return 0
    print(corpus.format_report(corpus.report(path)))
    return 0


def cmd_corpus_classify(args):
    path = _store_or_absent()
    if path is None:
        return 1
    n = classify.classify(path, args.family, batch=args.batch)
    print(f"{args.family} classified {n} cause(s)")
    return 0


def cmd_corpus_check(_args):
    path = _store_or_absent()
    if path is None:
        return 0
    problems = corpus.check(path)
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(f"corpus check: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("corpus check: ok")
    return 0


def cmd_corpus_disagreements(_args):
    path = _store_or_absent()
    if path is None:
        return 0
    with open(os.path.join(path, corpus.DISAGREEMENTS), "w", encoding="utf-8") as fh:
        fh.write(corpus.render_disagreements(path))
    print(f"wrote {corpus.DISAGREEMENTS} ({len(corpus.disagreements(path))} rows)")
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
    co = groups.add_parser("corpus", help="the corpus of shipped defects")
    co_cmds = co.add_subparsers(dest="command", required=True)
    co_cmds.add_parser("report", help="recoverable share and classification").set_defaults(
        func=cmd_corpus_report
    )
    co_cmds.add_parser("check", help="every source maps to one cause").set_defaults(
        func=cmd_corpus_check
    )
    co_cmds.add_parser("disagreements", help="write the file put to the author").set_defaults(
        func=cmd_corpus_disagreements
    )
    cl = co_cmds.add_parser("classify", help="classify unclassified causes with one family")
    cl.add_argument("--family", required=True, choices=["claude", "gpt"])
    cl.add_argument("--batch", type=int, default=25)
    cl.set_defaults(func=cmd_corpus_classify)
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)

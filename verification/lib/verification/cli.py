"""Command dispatch. Every gate is a subcommand that exits non-zero on failure."""

import argparse
import os
import sys

from . import classify, corpus, derive, retrieval, store, terms, units, violate


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


def cmd_terms_check(args):
    with open(args.spec, encoding="utf-8") as fh:
        problems = terms.check(fh.read(), store.location(), args.spec)
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(f"terms check: {len(problems)} unresolved", file=sys.stderr)
        return 1
    print("terms check: ok")
    return 0


def cmd_terms_apply(args):
    with open(args.spec, encoding="utf-8") as fh:
        text = fh.read()
    new, applied = terms.apply(text, store.location())
    if applied:
        with open(args.spec, "w", encoding="utf-8") as fh:
            fh.write(new)
    for term in applied:
        print(f"house-definition: {term}")
    print(f"terms apply: {len(applied)} term(s) resolved from the store")
    return 0


def cmd_terms_define(args):
    path = store.location()
    if path is None:
        print("store absent; cannot record a house definition", file=sys.stderr)
        return 1
    ctx = [c.strip() for c in args.context.split(",") if c.strip()]
    try:
        row = terms.define(path, args.term, ctx, args.definition, args.decided_by, args.origin)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"recorded {row['id']}")
    return 0


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _report(name, problems):
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(f"{name}: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print(f"{name}: ok")
    return 0


def cmd_premises_check(args):
    return _report("premises check", units.check_premises(_read(args.file), store.location()))


def cmd_premises_seed(_args):
    path = _store_or_absent()
    if path is None:
        return 1
    units.seed_questions(path)
    print("wrote premise_questions.jsonl")
    return 0


def cmd_claims_list(args):
    text = _read(args.file)
    for n, cid, claim, how in units.list_claims(text):
        print(f"issue {n}\t{cid}\t{claim}\t{how or '(no way of being false)'}")
    return _report("claims list", units.check_claims(text))


def cmd_closure_check(args):
    return _report("closure check", units.check_closure(_read(args.file)))


def _csv(value):
    return [x.strip() for x in (value or "").split(",") if x.strip()]


def cmd_retrieve(args):
    if not args.report:
        path = store.location()
        shapes, contexts = _csv(args.shape), _csv(args.context) + _csv(args.moved_from)
        unknown = store.unknown_keys(store.vocabulary(path), shapes, contexts) if path else []
        if unknown:
            return _report("retrieve", unknown)
        found = retrieval.query(path, shapes, _csv(args.context), args.moved_from)
        retrieval.record(args.unit, found)
        for e in found:
            print(f"{e['id']}\t{e['violation']}")
    counts, problems = retrieval.report(args.unit)
    print(" ".join(f"{k}={v}" for k, v in counts.items()))
    return _report("retrieve", problems) if args.report else 0


def cmd_derive(args):
    if not args.report:
        derive.derive(args.unit, args.spec)
    counts, problems = derive.report(args.unit)
    print(" ".join(f"{k}={v}" for k, v in counts.items()))
    return _report("derive", problems)


def cmd_violate(args):
    decl = violate.load(args.declaration)
    report, problems = violate.violate(decl)
    for line in report:
        print(line)
    return _report("violate", problems)


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
    te = groups.add_parser("terms", help="the term table and house definitions")
    te_cmds = te.add_subparsers(dest="command", required=True)
    tc = te_cmds.add_parser("check", help="every term resolved")
    tc.add_argument("spec")
    tc.set_defaults(func=cmd_terms_check)
    ta = te_cmds.add_parser("apply", help="resolve terms from house definitions")
    ta.add_argument("spec")
    ta.set_defaults(func=cmd_terms_apply)
    td = te_cmds.add_parser("define", help="record an author's resolution")
    td.add_argument("--term", required=True)
    td.add_argument("--context", required=True, help="comma-separated, e.g. xnys,us-equities")
    td.add_argument("--definition", required=True)
    td.add_argument("--decided-by", required=True)
    td.add_argument("--origin", required=True, help="pointer to the spec that resolved it")
    td.set_defaults(func=cmd_terms_define)
    pr = groups.add_parser("premises", help="premise statements in issue bodies")
    pr_cmds = pr.add_subparsers(dest="command", required=True)
    pc = pr_cmds.add_parser("check", help="every input answers every question")
    pc.add_argument("file", help="plan.md or one issue body")
    pc.set_defaults(func=cmd_premises_check)
    pr_cmds.add_parser("seed", help="write the question set to the store").set_defaults(
        func=cmd_premises_seed
    )
    cm = groups.add_parser("claims", help="claims in issue bodies")
    cm_cmds = cm.add_subparsers(dest="command", required=True)
    cmlist = cm_cmds.add_parser("list", help="list claims; fail on one that cannot be false")
    cmlist.add_argument("file")
    cmlist.set_defaults(func=cmd_claims_list)
    cl2 = groups.add_parser("closure", help="which issue closes each premise and claim")
    cl2_cmds = cl2.add_subparsers(dest="command", required=True)
    cc = cl2_cmds.add_parser("check", help="every item closed by exactly one issue")
    cc.add_argument("file", help="plan.md")
    cc.set_defaults(func=cmd_closure_check)
    rt = groups.add_parser("retrieve", help="store entries for a unit, and their disposition")
    rt.add_argument("--unit", required=True, help="the work unit directory")
    rt.add_argument("--shape", help="comma-separated shapes of the work")
    rt.add_argument("--context", help="comma-separated contexts (venue, asset class, source)")
    rt.add_argument("--moved-from", help="the context code or method is being moved from")
    rt.add_argument("--report", action="store_true", help="counts; fail on undisposed entries")
    rt.set_defaults(func=cmd_retrieve)
    dv = groups.add_parser("derive", help="premises, claims, failure cases on both families")
    dv.add_argument("--unit", required=True)
    dv.add_argument("--spec", help="spec.md the derivation reads (required unless --report)")
    dv.add_argument("--report", action="store_true")
    dv.set_defaults(func=cmd_derive)
    vi = groups.add_parser("violate", help="run a test on its violated variant and on correct code")
    vi.add_argument("declaration", help="JSON declaring the test, producer, variant and fixture")
    vi.set_defaults(func=cmd_violate)
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)

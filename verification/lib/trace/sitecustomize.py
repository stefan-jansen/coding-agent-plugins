"""Loaded at interpreter start by every Python process `verification violate` runs, through
PYTHONPATH: records which code ran, in the test process and in every child it starts.

A pipeline runner that starts each stage as `python stage.py` runs the producer in a child
process; a trace of the test process alone reports such a producer as never executed.

When $VERIFICATION_TRACE_DIR is set, each process writes <pid>.json there at exit:
    {"functions": [[file, name], ...], "lines": [[file, line], ...]}
Functions are every Python function or module body that started. Lines are recorded only for
the file:line pairs listed in $VERIFICATION_TRACE_LINES (comma-separated), which is where a
code mutation was applied. A child that ends with os._exit (a multiprocessing worker) or is
killed writes nothing. Any sitecustomize later on sys.path still runs.
"""

import atexit
import importlib.util
import json
import os
import sys

_functions = set()
_lines = set()
_watched = {}


def _watch():
    for item in filter(None, os.environ.get("VERIFICATION_TRACE_LINES", "").split(",")):
        path, _, line = item.rpartition(":")
        _watched.setdefault(os.path.realpath(path), set()).add(int(line))


def _start_monitoring():
    mon = sys.monitoring
    tool = next(t for t in range(6) if mon.get_tool(t) is None)
    mon.use_tool_id(tool, "verification-trace")

    def on_start(code, offset):
        _functions.add((os.path.realpath(code.co_filename), code.co_name))
        return mon.DISABLE

    def on_line(code, line):
        lines = _watched.get(os.path.realpath(code.co_filename))
        if lines and line in lines:
            _lines.add((os.path.realpath(code.co_filename), line))
        return mon.DISABLE

    mon.register_callback(tool, mon.events.PY_START, on_start)
    events = mon.events.PY_START
    if _watched:
        mon.register_callback(tool, mon.events.LINE, on_line)
        events |= mon.events.LINE
    mon.set_events(tool, events)


def _start_tracing():
    def local(frame, event, arg):
        if event == "line":
            path = os.path.realpath(frame.f_code.co_filename)
            if frame.f_lineno in _watched.get(path, ()):
                _lines.add((path, frame.f_lineno))
        return local

    def call(frame, event, arg):
        path = os.path.realpath(frame.f_code.co_filename)
        _functions.add((path, frame.f_code.co_name))
        return local if path in _watched else None

    sys.settrace(call)


def _dump(directory):
    with open(os.path.join(directory, f"{os.getpid()}.json"), "w", encoding="utf-8") as fh:
        json.dump({"functions": sorted(_functions), "lines": sorted(_lines)}, fh)


def _chain():
    """Run the sitecustomize this module shadows, if one is further down sys.path."""
    here = os.path.dirname(os.path.realpath(__file__))
    for entry in sys.path:
        if not entry or os.path.realpath(entry) == here:
            continue
        candidate = os.path.join(entry, "sitecustomize.py")
        if os.path.isfile(candidate):
            spec = importlib.util.spec_from_file_location("_shadowed_sitecustomize", candidate)
            spec.loader.exec_module(importlib.util.module_from_spec(spec))
            return


_directory = os.environ.get("VERIFICATION_TRACE_DIR")
if _directory and os.path.isdir(_directory):
    _watch()
    if hasattr(sys, "monitoring"):
        _start_monitoring()
    else:
        _start_tracing()
    atexit.register(_dump, _directory)
_chain()

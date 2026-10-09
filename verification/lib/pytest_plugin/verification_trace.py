"""Pytest plugin loaded by `verification violate`: records which code the test run executed.

It writes JSON to $VERIFICATION_TRACE_OUT at the end of the session:
    {"functions": [[file, name], ...], "lines": [[file, line], ...]}
Functions are every Python function or module body that started. Lines are recorded only for
the file:line pairs listed in $VERIFICATION_TRACE_LINES (comma-separated), which is where a
code mutation was applied.
"""

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


def pytest_configure(config):
    _watch()
    if hasattr(sys, "monitoring"):
        _start_monitoring()
    else:
        _start_tracing()


def pytest_unconfigure(config):
    out = os.environ.get("VERIFICATION_TRACE_OUT")
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"functions": sorted(_functions), "lines": sorted(_lines)}, fh)

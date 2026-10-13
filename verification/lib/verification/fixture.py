"""`verification fixture reduce`: write a filtered copy of a parquet or CSV file as a reduced
fixture.

The filter is a polars expression, evaluated by the project's interpreter (`--python`), since
the plugin itself is stdlib only. The copy is written beside its destination and moved into
place only when it is at most 10 MB; a larger one is deleted and refused. Whether the reduction
still holds what a test's violation needs is decided by `verification violate` with the copy
listed under `fixtures`, not here.
"""

import os
import subprocess
import tempfile

from .violate import FIXTURE_LIMIT

SCRIPT = """
import sys
import polars as pl

src, out, expr = sys.argv[1:4]
read = pl.read_csv if src.endswith(".csv") else pl.read_parquet
frame = read(src)
kept = frame.filter(eval(expr, {"pl": pl}))
if out.endswith(".csv"):
    kept.write_csv(out)
else:
    kept.write_parquet(out)
print(f"{kept.height} of {frame.height} rows")
"""


def reduce(src, dst, expr, python):
    """(ok, message)."""
    directory = os.path.dirname(os.path.abspath(dst))
    os.makedirs(directory, exist_ok=True)
    suffix = ".csv" if dst.endswith(".csv") else ".parquet"
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".reduce-", suffix=suffix)
    os.close(fd)
    try:
        proc = subprocess.run(
            [python, "-c", SCRIPT, src, tmp, expr], capture_output=True, text=True
        )
        if proc.returncode != 0:
            return False, proc.stderr.strip().splitlines()[-1] if proc.stderr else "failed"
        size = os.path.getsize(tmp)
        if size > FIXTURE_LIMIT:
            return False, f"{dst}: {size / 2**20:.1f} MB is over 10 MB; narrow the filter"
        os.replace(tmp, dst)
        return True, f"{dst}: {proc.stdout.strip()}, {size / 2**20:.2f} MB"
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

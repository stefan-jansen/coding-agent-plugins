"""`verification fixture reduce`: a filtered copy of a data file, refused above 10 MB.

The filter runs under the project's interpreter, which must have polars. Set
VERIFICATION_POLARS_PYTHON to one (for example a project's .venv/bin/python) to run these.
"""

import os
import subprocess
import sys

import pytest

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")
PY = os.environ.get("VERIFICATION_POLARS_PYTHON")

pytestmark = pytest.mark.skipif(not PY, reason="VERIFICATION_POLARS_PYTHON is not set")


def polars(code):
    subprocess.run([PY, "-c", code], check=True)


def reduce(src, dst, expr):
    return subprocess.run(
        [
            sys.executable,
            BIN,
            "fixture",
            "reduce",
            str(src),
            str(dst),
            "--filter",
            expr,
            "--python",
            PY,
        ],
        capture_output=True,
        text=True,
    )


def test_a_parquet_file_is_reduced_to_the_filtered_rows(tmp_path):
    src, dst = tmp_path / "bars.parquet", tmp_path / "small" / "bars.parquet"
    polars(f"import polars as pl; pl.DataFrame({{'t': range(100)}}).write_parquet({str(src)!r})")
    r = reduce(src, dst, 'pl.col("t") < 10')
    assert r.returncode == 0, r.stderr
    assert "10 of 100 rows" in r.stdout
    polars(f"import polars as pl; assert pl.read_parquet({str(dst)!r}).height == 10")


def test_a_reduction_over_10_mb_is_refused_and_leaves_nothing(tmp_path):
    # Prevents: a "reduced" fixture that is as large as the data it replaces (criterion 16).
    src, dst = tmp_path / "wide.csv", tmp_path / "out" / "wide.csv"
    polars(
        "import polars as pl; pl.DataFrame({'t': range(800_000), 's': ['x' * 12] * 800_000})"
        f".write_csv({str(src)!r})"
    )
    r = reduce(src, dst, "pl.lit(True)")
    assert r.returncode == 1
    assert "over 10 MB" in r.stderr
    assert not dst.exists()
    assert not list((tmp_path / "out").iterdir())

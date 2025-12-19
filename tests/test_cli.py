import subprocess
import sys
from pathlib import Path


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    """
    Запускаем CLI как модуль: python -m fileflow.cli ...
    Возвращаем CompletedProcess со stdout/stderr и returncode.
    """
    cmd = [sys.executable, "-m", "fileflow.cli", *args]
    return subprocess.run(cmd, text=True, capture_output=True)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_cli_run_prints_to_stdout(tmp_path: Path) -> None:
    inp = tmp_path / "in.txt"
    write_text(inp, "a\n\n  b  \n")

    # run INPUT --strip --drop-empty
    res = run_cli(["run", str(inp), "--strip", "--drop-empty"])

    assert res.returncode == 0
    assert res.stdout.strip() == "a\nb"
    assert "Steps:" in res.stderr

def test_cli_run_writes_to_file_when_out_is_provided(tmp_path: Path) -> None:
    inp = tmp_path / "in.txt"
    out = tmp_path / "out.txt"
    write_text(inp, "gral\nok\n")

    res = run_cli(["run", str(inp), "--out", str(out), "--replace", "gral", "GRAL"])

    assert res.returncode == 0
    assert out.read_text(encoding="utf-8").strip() == "GRAL\nok"
    assert res.stdout == ""  # когда пишем в файл, stdout должен быть пустым
    assert "Steps:" in res.stderr

def test_cli_head_rejects_non_positive_value(tmp_path: Path) -> None:
    inp = tmp_path / "in.txt"
    write_text(inp, "a\nb\n")

    res = run_cli(["run", str(inp), "--head", "0"])

    assert res.returncode != 0
    assert "--head N: N must be a positive integer" in res.stderr

def test_cli_grep_filters_lines(tmp_path):
    inp = tmp_path / "in.txt"
    inp.write_text(
        "error: file not found\n"
        "ok\n"
        "error: permission denied\n",
        encoding="utf-8",
    )

    res = run_cli(["run", str(inp), "--grep", "error"])

    assert res.returncode == 0
    assert res.stdout.strip() == (
        "error: file not found\n"
        "error: permission denied"
    )
    assert "GrepProcessor" in res.stderr
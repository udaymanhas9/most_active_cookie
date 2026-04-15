"""End-to-end tests for the CLI entry point."""

import pathlib
import subprocess
import sys

import pytest

SAMPLE_LOG = """\
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00
"""

CLI_PATH = str(pathlib.Path(__file__).parent.parent / "cli.py")


@pytest.fixture
def log_file(tmp_path) -> str:
    """Write the sample log to a temp file and return its path."""
    path = tmp_path / "cookie_log.csv"
    path.write_text(SAMPLE_LOG)
    return str(path)


def run_cli(*args) -> subprocess.CompletedProcess[str]:
    """Run the CLI as a subprocess and return the result."""
    return subprocess.run(
        [sys.executable, CLI_PATH, *args],
        capture_output=True,
        text=True,
    )


class TestCLISingleWinner:
    """Tests where one cookie is most active."""

    def test_dec_09_returns_most_active(self, log_file: str):
        result = run_cli("-f", log_file, "-d", "2018-12-09")
        assert result.returncode == 0
        assert result.stdout.strip() == "AtY0laUfhglK3lC7"

    def test_dec_07_returns_single_cookie(self, log_file: str):
        result = run_cli("-f", log_file, "-d", "2018-12-07")
        assert result.returncode == 0
        assert result.stdout.strip() == "4sMM2LxV07bPJzwf"


class TestCLITiedWinners:
    """Tests where multiple cookies tie for most active."""

    def test_dec_08_returns_all_tied(self, log_file: str):
        result = run_cli("-f", log_file, "-d", "2018-12-08")
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert sorted(lines) == sorted(
            [
                "SAZuXPGUrfbcn5UA",
                "4sMM2LxV07bPJzwf",
                "fbcn5UAVanZf6UtG",
            ]
        )


class TestCLIEdgeCases:
    """Tests for edge cases and error handling."""

    def test_no_entries_for_date_produces_no_output(self, log_file: str):
        result = run_cli("-f", log_file, "-d", "2018-12-01")
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_missing_file_returns_error(self):
        result = run_cli("-f", "/nonexistent/file.csv", "-d", "2018-12-09")
        assert result.returncode != 0
        assert "not found" in result.stderr.lower()

    def test_missing_required_args(self):
        result = run_cli()
        assert result.returncode != 0

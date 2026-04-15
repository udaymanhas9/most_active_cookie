"""Tests for the CookieLog reader and filter."""

import pytest
from cookie_log import CookieLog

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


@pytest.fixture
def sample_log_file(tmp_path) -> str:
    """Write the sample log to a temp file and return its path."""
    path = tmp_path / "cookie_log.csv"
    path.write_text(SAMPLE_LOG)
    return str(path)


@pytest.fixture
def cookie_log(sample_log_file: str) -> CookieLog:
    """Return a CookieLog loaded from the sample data."""
    return CookieLog(sample_log_file)


class TestCookieLogLoading:
    """Tests for file loading behaviour."""

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            CookieLog("/nonexistent/path.csv")

    def test_empty_file_loads(self, tmp_path):
        path = tmp_path / "empty.csv"
        path.write_text("cookie,timestamp\n")
        log = CookieLog(str(path))
        assert log.get_cookies_for_date("2018-12-09") == []

    def test_header_only_no_newline(self, tmp_path):
        path = tmp_path / "header.csv"
        path.write_text("cookie,timestamp")
        log = CookieLog(str(path))
        assert log.get_cookies_for_date("2018-12-09") == []


class TestGetCookiesForDate:
    """Tests for date-filtered cookie retrieval."""

    def test_single_winner_date(self, cookie_log: CookieLog):
        cookies = cookie_log.get_cookies_for_date("2018-12-09")
        assert cookies == [
            "AtY0laUfhglK3lC7",
            "SAZuXPGUrfbcn5UA",
            "5UAVanZf6UtGyKVS",
            "AtY0laUfhglK3lC7",
        ]

    def test_returns_all_cookies_for_tied_date(self, cookie_log: CookieLog):
        cookies = cookie_log.get_cookies_for_date("2018-12-08")
        assert cookies == [
            "SAZuXPGUrfbcn5UA",
            "4sMM2LxV07bPJzwf",
            "fbcn5UAVanZf6UtG",
        ]

    def test_single_entry_date(self, cookie_log: CookieLog):
        cookies = cookie_log.get_cookies_for_date("2018-12-07")
        assert cookies == ["4sMM2LxV07bPJzwf"]

    def test_no_entries_for_date(self, cookie_log: CookieLog):
        assert cookie_log.get_cookies_for_date("2018-12-01") == []

    def test_future_date_returns_empty(self, cookie_log: CookieLog):
        assert cookie_log.get_cookies_for_date("2025-01-01") == []


class TestEarlyExit:
    """Verify early termination doesn't skip valid entries."""

    def test_does_not_include_older_dates(self, cookie_log: CookieLog):
        cookies = cookie_log.get_cookies_for_date("2018-12-09")
        # Should not contain any cookies from 2018-12-08 or earlier
        dec08_cookies = {"SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf", "fbcn5UAVanZf6UtG"}
        # SAZuXPGUrfbcn5UA appears on both dates, so check the count
        assert len(cookies) == 4  # exactly 4 entries on Dec 9

    def test_middle_date_gets_only_its_entries(self, cookie_log: CookieLog):
        cookies = cookie_log.get_cookies_for_date("2018-12-08")
        assert "AtY0laUfhglK3lC7" not in cookies  # Dec 9 cookie excluded
        assert "4sMM2LxV07bPJzwf" in cookies

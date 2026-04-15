"""Tests for the CookieEntry model."""

import pytest
from models import CookieEntry


class TestCookieEntryFromRawLine:
    """Tests for the from_raw_line factory method."""

    def test_parses_valid_line(self):
        entry = CookieEntry.from_raw_line("AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00")
        assert entry.cookie == "AtY0laUfhglK3lC7"
        assert entry.date == "2018-12-09"

    def test_strips_whitespace_and_newline(self):
        entry = CookieEntry.from_raw_line(
            "  SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00  \n"
        )
        assert entry.cookie == "SAZuXPGUrfbcn5UA"
        assert entry.date == "2018-12-08"

    def test_malformed_line_raises_error(self):
        with pytest.raises(ValueError):
            CookieEntry.from_raw_line("no_comma_here")


class TestCookieEntryImmutability:
    """Tests that CookieEntry is frozen"""

    def test_cannot_modify_cookie(self):
        entry = CookieEntry(cookie="abc", date="2018-12-09")
        with pytest.raises(AttributeError):
            entry.cookie = "xyz"

    def test_cannot_modify_date(self):
        entry = CookieEntry(cookie="abc", date="2018-12-09")
        with pytest.raises(AttributeError):
            entry.date = "2020-01-01"

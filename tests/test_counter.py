"""Tests for the CookieCounter class."""

from counter import CookieCounter


class TestMostActive:
    """Tests for most_active cookie determination."""

    def test_single_most_active(self):
        cookies = ["aaa", "bbb", "aaa", "ccc"]
        result = CookieCounter(cookies).most_active()
        assert result == ["aaa"]

    def test_multiple_tied_cookies(self):
        cookies = ["aaa", "bbb", "ccc"]
        result = CookieCounter(cookies).most_active()
        assert sorted(result) == ["aaa", "bbb", "ccc"]

    def test_two_way_tie(self):
        cookies = ["aaa", "bbb", "aaa", "bbb", "ccc"]
        result = CookieCounter(cookies).most_active()
        assert sorted(result) == ["aaa", "bbb"]

    def test_single_entry(self):
        result = CookieCounter(["only_one"]).most_active()
        assert result == ["only_one"]

    def test_empty_input(self):
        result = CookieCounter([]).most_active()
        assert result == []

    def test_all_same_cookie(self):
        cookies = ["aaa", "aaa", "aaa"]
        result = CookieCounter(cookies).most_active()
        assert result == ["aaa"]

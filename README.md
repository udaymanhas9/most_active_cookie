# Most Active Cookie

Command line tool that finds the most active cookie in a log file for a given day.

Takes a CSV log of cookies and timestamps, filters by a specified date, and returns the cookie(s) that appeared the most. If multiple cookies are tied, all of them are printed on separate lines.

The log file is expected to be sorted by timestamp (most recent first), which the programme takes advantage of for early termination.

## Requirements

- Python 3.13.5

```
pip install -e ".[dev]"
```

## Usage

```
python3 cli.py -f cookie_log.csv -d 2018-12-09
```

Or make it executable first:

```
chmod +x cli.py
./cli.py -f cookie_log.csv -d 2018-12-09
```

Or use the bash wrapper:

```
chmod +x most_active_cookie
./most_active_cookie -f cookie_log.csv -d 2018-12-09
```

## Running Tests

```
python -m pytest tests/ -v
```

## Project Structure

```
most_active_cookie/
├── cli.py              # Entry point, argument parsing
├── models.py           # CookieEntry dataclass
├── cookie_log.py       # Reads CSV, filters entries by date
├── counter.py          # Counts cookies, finds most active
├── most_active_cookie  # Bash wrapper script
└── tests/
    ├── conftest.py         # Path setup for imports
    ├── test_models.py      # CookieEntry parsing and immutability
    ├── test_cookie_log.py  # File loading, date filtering, early exit
    ├── test_counter.py     # Counting logic and tie handling
    └── test_cli.py         # End-to-end CLI tests via subprocess
```

## CFB Rankings – Public API and Usage Guide

This repository contains a lightweight pipeline for collecting College Football (CFB) schedule data, normalizing school names, storing data in SQLite, and computing simple running rankings. This README documents all public modules and functions with clear usage examples.

- **Language**: Python 3.9+
- **Data store**: SQLite (`db/schools.db`)
- **Key dependencies**: `requests`, `pandas`, `beautifulsoup4`

### Install dependencies

```bash
pip install requests pandas beautifulsoup4
```

### Repository structure

```
db/
  db.py                    # SQLite helpers (connect, create, insert, query, etc.)
data/
  download.py              # Utility to download reference files
fetchers_cfb.py            # Scraper for Sports-Reference schedule with ID enrichment
ranking_system.py          # Running rankings based on margin of victory
school_naming_information.py # Name normalization and schedule update via IDs
testing/
  school_naming_information_testing.py
```

Note: `fetchers_cfb.py` contains top-level executable code that will perform network requests and DB inserts when the module is imported. Prefer running it as a script (e.g., `python fetchers_cfb.py`).

---

## Module: `db/db.py`

SQLite helper functions to connect, create tables, insert data, query, and inspect schema.

### connect_to_db(db_name: str) -> sqlite3.Connection | None
Connect to a SQLite database by relative path (joined to current working directory). Returns a connection or `None` on error.

```python
from db.db import connect_to_db, close_connection

conn = connect_to_db("db/schools.db")
try:
    # use conn
    pass
finally:
    if conn:
        close_connection(conn)
```

### create_table(conn, column_names: list, table_name: str) -> None
Create a table with the provided column names. Column names are quoted to allow spaces.

```python
from db.db import connect_to_db, create_table

conn = connect_to_db("db/schools.db")
create_table(conn, ["Winner", "Loser", "Winner Points"], "schedule")
```

### insert_data_into_table(conn, data_dic: dict, table_name: str) -> None
Insert rows from a dictionary-of-lists into a table. Strings are safely quoted; NaN becomes NULL.

```python
from db.db import connect_to_db, insert_data_into_table

rows = {
    "Winner": ["Georgia", "Ohio State"],
    "Loser": ["Alabama", "Michigan"],
    "Winner Points": [27, 31]
}
conn = connect_to_db("db/schools.db")
insert_data_into_table(conn, rows, "schedule")
```

### query_db(conn, query: str) -> dict | None
Execute a SQL query and return a dict mapping column name to list of values, or `None` on failure.

```python
from db.db import connect_to_db, query_db

conn = connect_to_db("db/schools.db")
result = query_db(conn, "SELECT Winner, Loser FROM schedule LIMIT 5")
print(result)  # {"Winner": [..], "Loser": [..]}
```

### get_last_row(conn, table_name: str) -> dict | None
Return the last row by ROWID as `{0: tuple_of_values}` or `None` on error.

```python
from db.db import connect_to_db, get_last_row

conn = connect_to_db("db/schools.db")
last = get_last_row(conn, "schedule")
print(last)
```

### get_length_of_table(conn, table_name: str) -> int | None
Return row count for the table or `None` on error.

```python
from db.db import connect_to_db, get_length_of_table

conn = connect_to_db("db/schools.db")
print(get_length_of_table(conn, "schedule"))
```

### close_connection(conn) -> None
Close the provided SQLite connection.

```python
from db.db import connect_to_db, close_connection

conn = connect_to_db("db/schools.db")
close_connection(conn)
```

### db_info(conn) -> None
Print all table names and their column names.

```python
from db.db import connect_to_db, db_info

conn = connect_to_db("db/schools.db")
db_info(conn)
```

---

## Module: `school_naming_information.py`

Utilities for mapping month abbreviations, resolving school canonical names and IDs from the database, and updating a schedule CSV with IDs.

### month_number_from_month_abbreviation(month_abbreviation: str) -> int
Convert a month abbreviation to a 1–12 integer. Accepts case-insensitive values among `{jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec}`. Raises `ValueError` if invalid.

```python
from school_naming_information import month_number_from_month_abbreviation

assert month_number_from_month_abbreviation("Sep") == 9
assert month_number_from_month_abbreviation("dec") == 12
```

### get_school_naming_infomation(school_name: str) -> tuple[str, list[str], int] | None
Look up a school by canonical name or by alias. Returns `(canonical_name, aliases_list, ID)` or `None` if not found. The function attempts several database paths to be resilient to working directory differences.

```python
from school_naming_information import get_school_naming_infomation

info = get_school_naming_infomation("Ole Miss")
if info is None:
    print("School not found")
else:
    canonical, aliases, school_id = info
    print(canonical, aliases, school_id)
```

### update_schedule_with_ID_information() -> None
Load `data/schedule.csv`, normalize columns, look up Winner/Loser IDs, and write a `schedule` table to SQLite. Expects `db/schools.db` and `data/schedule.csv` to exist.

```python
from school_naming_information import update_schedule_with_ID_information

# Ensure data/schedule.csv exists and db/schools.db is accessible
update_schedule_with_ID_information()
```

---

## Module: `fetchers_cfb.py`

Scraper for Sports-Reference schedule pages that parses weekly results and enriches with school IDs via `get_school_naming_infomation`.

Important: This file contains top-level code that will execute when imported:
- It calls `fetch_schedule(2023)` and writes rows into the `schedule` table of `db/schools.db`.

Prefer running it directly: `python fetchers_cfb.py`.

### check_url(url: str) -> bool
Return `True` if a GET request returns HTTP 200, else `False`.

```python
from fetchers_cfb import check_url

ok = check_url("https://www.sports-reference.com/cfb/years/2023-schedule.html")
print(ok)
```

### fetch_schedule(YEAR: int) -> dict | None
Fetch and parse the season schedule from Sports-Reference. Returns a dictionary-of-lists with columns:
`[Winner, Loser, Winner Points, Loser Points, Location, Date, Time, Day, Week, Year, Month, Day, Winner ID, Loser ID]`.

Skips games with missing or zero scores. Strips AP ranking prefixes from team names.

```python
from fetchers_cfb import fetch_schedule

data_dict = fetch_schedule(2023)
print(list(data_dict.keys()))
print({k: v[:2] for k, v in data_dict.items()})  # preview first two rows per column
```

Insert into DB example:

```python
from db.db import connect_to_db, insert_data_into_table, close_connection
from fetchers_cfb import fetch_schedule

data_dict = fetch_schedule(2023)
conn = connect_to_db("db/schools.db")
insert_data_into_table(conn, data_dict, "schedule")
close_connection(conn)
```

---

## Module: `ranking_system.py`

Compute running rankings based on margin-of-victory buckets. Reads from the `schedule` table for a given season window (Aug–Jul style year span).

### calculate_margin_of_victory_score(Winning_Team_Points, Losing_Team_Points) -> float
Bucketed scoring based on the point margin, returning values in `[0.5, 1, 2, 4, 5, 6, 7, 8]`.

```python
from ranking_system import calculate_margin_of_victory_score

assert calculate_margin_of_victory_score(31, 28) == 0.5
assert calculate_margin_of_victory_score(42, 14) == 7
```

### calculate_running_rankings(year: int) -> dict[str, float]
Aggregate margin-of-victory scores across all games within the season window for `year`. Positive scores for winners, negative for losers.

```python
from ranking_system import calculate_running_rankings

rankings = calculate_running_rankings(2023)
print(sorted(rankings.items(), key=lambda x: x[1], reverse=True)[:10])
```

### calculate_rankings_with_previous_year(year: int, running_rankings: dict[str, float]) -> dict[str, float]
Recompute the same season window and add to an existing `running_rankings` dict—useful for blending prior-year performance.

```python
from ranking_system import calculate_running_rankings, calculate_rankings_with_previous_year

current = calculate_running_rankings(2023)
blended = calculate_rankings_with_previous_year(2022, current)
print(sorted(blended.items(), key=lambda x: x[1], reverse=True)[:10])
```

---

## Module: `data/download.py`

Utility for downloading reference files.

### download_college_names_file(url: str, filename: str = "names.txt") -> None
Download a plain-text college names file and save it locally.

```python
from data.download import download_college_names_file

download_college_names_file(
    url="https://talismanred.com/ratings/cf/wilson/names.txt",
    filename="names.txt",
)
```

---

## Quick start: end-to-end

1) Ensure `db/schools.db` exists and contains `schools` metadata (canonical names, aliases, IDs).
2) Populate the `schedule` table by either:
   - Running the scraper: `python fetchers_cfb.py` (inserts 2023 schedule as written), or
   - Preparing `data/schedule.csv` and running `update_schedule_with_ID_information()`.
3) Compute rankings for a year:

```python
from ranking_system import calculate_running_rankings

rankings = calculate_running_rankings(2023)
print(sorted(rankings.items(), key=lambda x: x[1], reverse=True)[:15])
```

### Notes and caveats

- `fetchers_cfb.py` performs network I/O and DB writes at import time; run it as a script to avoid side effects.
- The ranking functions assume numeric point values in the DB. Ensure ETL steps preserve numeric types.
- `get_school_naming_infomation` tries multiple DB paths; prefer running from the repository root.

---

## Testing

Basic tests for school naming are in `testing/school_naming_information_testing.py`. You can run them with any Python test runner (e.g., `pytest`) after installing dependencies.

```bash
pytest -q
```

---

## License

No license specified. Add one if you intend to distribute or open source.
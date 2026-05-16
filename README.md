# json_query

**json_query** is a minimal command‑line tool written in Python that lets you safely extract data from JSON documents using [JMESPath](https://jmespath.org/) expressions.

### Features
- Reads JSON from a file or STDIN.
- Accepts a JMESPath query string to filter the document.
- Provides clear, user‑friendly error messages on:
  - Missing or unreadable input files.
  - Invalid JSON syntax.
  - Malformed JMESPath expressions.
- Idempotent: running the same command multiple times produces the same output without side effects.

### Installation
```bash
# Clone the repository (or copy the single file)
git clone https://example.com/json_query.git
cd json_query
# (Optional) Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate
# Install the only dependency
pip install jmespath
```

### Usage
```bash
# From a file
python3 json_query.py data.json "people[?age > `30`].name"

# From STDIN (e.g., piping data)
cat data.json | python3 json_query.py - "people[0]"
```

### Exit Codes
| Code | Meaning                              |
|------|--------------------------------------|
| 0    | Success                              |
| 1    | File‑related error (missing, unreadable) |
| 2    | JSON parsing error                  |
| 3    | JMESPath query error                |
| 4    | Unexpected internal error            |

### License
MIT – see `LICENSE` file in the repository.

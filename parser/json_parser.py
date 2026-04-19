import json
import os
from datetime import datetime


def parse_date(date_str):
    """Convert an ISO 8601 date string like '2021-10-30T...' to MM/DD/YYYY format."""
    if not date_str:
        return ""
    try:
        # Python's fromisoformat doesn't handle 'Z', so we replace it with '+00:00'
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%m/%d/%Y")
    except ValueError:
        # If the date format is unexpected, just return it as-is
        return date_str


def parse_json_file(filepath):
    """Read one JSON file and return a dictionary with the columns we want in the CSV."""

    # Open and load the JSON file into a Python dictionary
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build and return a row for our CSV
    # .get("field", "") means: get this field, or use "" if it doesn't exist
    return {
        "Event":        data.get("headline", ""),      # The news headline
        "Event Title":  data.get("description", ""),   # A short summary of the article
        "News Body":    data.get("article", ""),        # The full article text
        "Url":          data.get("url", ""),            # Link to the original article
        "Corpora Name": data.get("source", ""),         # News source (e.g. "mzamin")
        "News Date":    parse_date(data.get("date_published", "")),  # Formatted date
        # These three columns are left empty for manual annotation later
        "Govt Leaning": "",
        "Govt Critics": "",
        "Neutral":      "",
    }


def parse_directory(input_dir):
    """Read all JSON files in a folder and return a list of rows (one row per file)."""
    records = []

    # sorted() makes sure files are processed in alphabetical order
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            try:
                record = parse_json_file(filepath)
                records.append(record)
            except Exception as e:
                # If a file has a problem, skip it and show a warning
                print(f"Skipping {filename}: {e}")

    return records

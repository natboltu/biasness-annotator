import os
import csv
from parser.json_parser import parse_directory

# ── Settings ──────────────────────────────────────────────────────────────────
# Change INPUT_DIR to point to whichever news folder you want to parse
INPUT_DIR  = "/Users/opuchakraborty/Work/mzamin"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "parsed_data.csv")

# These are the column headers that will appear in the CSV file
COLUMNS = [
    "Event",        # News headline
    "Event Title",  # Short summary
    "News Body",    # Full article text
    "Url",          # Link to the original article
    "Corpora Name", # News source name
    "News Date",    # Publication date (MM/DD/YYYY)
    "Govt Leaning", # ← Fill these in manually to annotate political bias
    "Govt Critics", # ←
    "Neutral",      # ←
]
# ──────────────────────────────────────────────────────────────────────────────


def write_csv(records, output_path):
    """Save a list of records (dictionaries) to a CSV file."""

    # 'utf-8-sig' adds a BOM byte at the start of the file.
    # This tells Excel and Google Sheets that the file uses Bengali (UTF-8) text.
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()   # Write the column titles on the first row
        writer.writerows(records)  # Write all data rows

    print(f"Done! CSV saved to: {output_path}")


def main():
    # Step 1: Make sure the output folder exists (create it if it doesn't)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 2: Read all JSON files from the input folder
    print(f"Reading JSON files from: {INPUT_DIR}")
    records = parse_directory(INPUT_DIR)
    print(f"Found and parsed {len(records)} articles.")

    # Step 3: Write everything to a CSV file
    write_csv(records, OUTPUT_FILE)


# This line means: only run main() when you run this file directly
# (not when it is imported by another script)
if __name__ == "__main__":
    main()

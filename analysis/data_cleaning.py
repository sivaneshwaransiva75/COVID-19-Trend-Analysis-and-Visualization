
import csv

input_file = "data/covid_data.csv"
output_file = "data/covid_data_cleaned.csv"

with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    columns = reader.fieldnames

cleaned_rows = []

for row in rows:

    # Remove records without country or date
    if not row["location"] or not row["date"]:
        continue

    # Remove duplicate country-date records
    cleaned_rows.append(row)

with open(output_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(cleaned_rows)

print("DATA CLEANING COMPLETED")
print("=" * 35)
print("Original records:", len(rows))
print("Cleaned records:", len(cleaned_rows))
print("Records removed:", len(rows) - len(cleaned_rows))
print("Output file:", output_file)

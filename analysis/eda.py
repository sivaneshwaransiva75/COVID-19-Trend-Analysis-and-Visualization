
import csv

file_path = "data/covid_data_cleaned.csv"

country_data = {}

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        country = row["location"]

        # Skip aggregate records without a continent
        if not row["continent"]:
            continue

        if country not in country_data:
            country_data[country] = {
                "cases": 0,
                "deaths": 0
            }

        cases = row["total_cases"]
        deaths = row["total_deaths"]

        if cases:
            country_data[country]["cases"] = max(
                country_data[country]["cases"], float(cases)
            )

        if deaths:
            country_data[country]["deaths"] = max(
                country_data[country]["deaths"], float(deaths)
            )

# Total countries
total_countries = len(country_data)

# Find highest cases and deaths
highest_cases = max(
    country_data.items(),
    key=lambda item: item[1]["cases"]
)

highest_deaths = max(
    country_data.items(),
    key=lambda item: item[1]["deaths"]
)

# Calculate worldwide totals using country-level maximum values
worldwide_cases = sum(
    data["cases"] for data in country_data.values()
)

worldwide_deaths = sum(
    data["deaths"] for data in country_data.values()
)

print("COVID-19 EXPLORATORY DATA ANALYSIS")
print("=" * 45)

print("Total Countries:", total_countries)
print("Total Confirmed Cases:", f"{worldwide_cases:,.0f}")
print("Total Deaths:", f"{worldwide_deaths:,.0f}")

print("\nCOUNTRY WITH HIGHEST CASES")
print(highest_cases[0])
print(f"Cases: {highest_cases[1]['cases']:,.0f}")

print("\nCOUNTRY WITH HIGHEST DEATHS")
print(highest_deaths[0])
print(f"Deaths: {highest_deaths[1]['deaths']:,.0f}")

print("\nEDA completed successfully!")

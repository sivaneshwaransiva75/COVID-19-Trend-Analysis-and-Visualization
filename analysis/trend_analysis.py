
import csv
import matplotlib.pyplot as plt

file_path = "data/covid_data_cleaned.csv"

country_data = {}

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        country = row["location"]

        if not row["continent"]:
            continue

        vaccinated = row["people_vaccinated"]
        population = row["population"]

        if not vaccinated or not population:
            continue

        vaccinated = float(vaccinated)
        population = float(population)

        if population <= 0:
            continue

        date = row["date"]

        if country not in country_data or date > country_data[country]["date"]:
            country_data[country] = {
                "date": date,
                "vaccinated": vaccinated,
                "population": population
            }

# Calculate vaccination coverage
vaccination_data = []

for country, data in country_data.items():

    coverage = (
        data["vaccinated"] / data["population"]
    ) * 100

    vaccination_data.append((country, coverage))

# Sort countries by coverage
top_countries = sorted(
    vaccination_data,
    key=lambda item: item[1],
    reverse=True
)[:10]

countries = [item[0] for item in top_countries]
coverage = [item[1] for item in top_countries]

# Display results
print("TOP 10 COUNTRIES BY VACCINATION COVERAGE")
print("=" * 50)

for rank, (country, percentage) in enumerate(top_countries, start=1):
    print(f"{rank}. {country}: {percentage:.2f}%")

# Create chart
plt.figure(figsize=(12, 6))

plt.bar(countries, coverage)

plt.title("Top 10 Countries by COVID-19 Vaccination Coverage")
plt.xlabel("Countries")
plt.ylabel("Population Vaccinated (%)")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("reports/top_10_vaccination_coverage.png")

plt.show()

print("\nVaccination analysis completed!")
print("Saved at: reports/top_10_vaccination_coverage.png")

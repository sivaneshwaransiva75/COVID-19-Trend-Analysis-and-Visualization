
import csv
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "covid_data_cleaned.csv")


# Convert CSV values into numbers
def convert_number(value):
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except (ValueError, TypeError):
        return None


# Load the latest record for each country
def load_country_data():

    countries = {}

    if not os.path.exists(DATA_FILE):
        return countries

    with open(DATA_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            country = row.get("location", "").strip()
            continent = row.get("continent", "").strip()
            date = row.get("date", "").strip()

            if not country or not continent or not date:
                continue

            if country not in countries or date > countries[country]["date"]:

                countries[country] = {
                    "date": date,
                    "cases": convert_number(row.get("total_cases")),
                    "deaths": convert_number(row.get("total_deaths")),
                    "new_cases": convert_number(row.get("new_cases")),
                    "new_deaths": convert_number(row.get("new_deaths")),
                    "vaccinated": convert_number(row.get("people_vaccinated")),
                    "fully_vaccinated": convert_number(
                        row.get("people_fully_vaccinated")
                    ),
                    "population": convert_number(row.get("population")),
                    "cases_per_million": convert_number(
                        row.get("total_cases_per_million")
                    ),
                    "deaths_per_million": convert_number(
                        row.get("total_deaths_per_million")
                    )
                }

    return countries


# Dashboard summary
def get_covid_summary(countries):

    total_cases = sum(
        (item["cases"] or 0) for item in countries.values()
    )

    total_deaths = sum(
        (item["deaths"] or 0) for item in countries.values()
    )

    return {
        "total_countries": len(countries),
        "total_cases": f"{total_cases:,.0f}",
        "total_deaths": f"{total_deaths:,.0f}"
    }


# Generate data insights
def get_data_insights(countries):

    valid_cases = {
        name: data for name, data in countries.items()
        if data["cases"] is not None
    }

    valid_deaths = {
        name: data for name, data in countries.items()
        if data["deaths"] is not None
    }

    valid_vaccination = {
        name: data for name, data in countries.items()
        if data["fully_vaccinated"] is not None
    }

    highest_cases = max(
        valid_cases.items(),
        key=lambda item: item[1]["cases"],
        default=None
    )

    highest_deaths = max(
        valid_deaths.items(),
        key=lambda item: item[1]["deaths"],
        default=None
    )

    highest_vaccination = max(
        valid_vaccination.items(),
        key=lambda item: item[1]["fully_vaccinated"],
        default=None
    )

    death_rates = []

    for country, data in countries.items():

        cases = data["cases"]
        deaths = data["deaths"]

        if cases is not None and deaths is not None and cases >= 100000:

            death_rates.append({
                "country": country,
                "death_rate": (deaths / cases) * 100
            })

    lowest_death_rate = min(
        death_rates,
        key=lambda item: item["death_rate"],
        default=None
    )

    return {

        "highest_cases": {
            "country": highest_cases[0],
            "value": highest_cases[1]["cases"]
        } if highest_cases else None,

        "highest_deaths": {
            "country": highest_deaths[0],
            "value": highest_deaths[1]["deaths"]
        } if highest_deaths else None,

        "highest_vaccination": {
            "country": highest_vaccination[0],
            "value": highest_vaccination[1]["fully_vaccinated"]
        } if highest_vaccination else None,

        "lowest_death_rate": lowest_death_rate
    }


# Dashboard page
@app.route("/")
@app.route("/dashboard")
def dashboard():

    countries = load_country_data()
    summary = get_covid_summary(countries)

    return render_template(
        "index.html",
        summary=summary,
        countries=sorted(countries.keys())
    )


# Individual country details API
@app.route("/api/country/<path:country>")
def country_details(country):

    countries = load_country_data()

    actual_country = next(
        (name for name in countries if name.lower() == country.lower()),
        None
    )

    if not actual_country:
        return jsonify({"error": "Country not found"}), 404

    return jsonify({
        "country": actual_country,
        **countries[actual_country]
    })


# Data insights API
@app.route("/api/insights")
def insights_api():

    countries = load_country_data()

    return jsonify(get_data_insights(countries))


# Historical country trend API
@app.route("/api/country-trend/<path:country>")
def country_trend(country):

    trend_data = []

    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "Dataset not found"}), 404

    with open(DATA_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            row_country = row.get("location", "").strip()
            continent = row.get("continent", "").strip()

            if (
                row_country.lower() == country.strip().lower()
                and continent
            ):

                trend_data.append({
                    "date": row.get("date"),
                    "total_cases": convert_number(row.get("total_cases")),
                    "new_cases": convert_number(row.get("new_cases")),
                    "total_deaths": convert_number(row.get("total_deaths"))
                })

    trend_data.sort(key=lambda item: item["date"] or "")

    if not trend_data:
        return jsonify({"error": "No trend data found"}), 404

    return jsonify({
        "country": country,
        "records": trend_data
    })


# Country comparison API
@app.route("/api/compare")
def compare_countries():

    try:

        country1 = request.args.get("country1", "").strip()
        country2 = request.args.get("country2", "").strip()

        if not country1 or not country2:
            return jsonify({
                "error": "Please select both countries."
            }), 400

        if country1.lower() == country2.lower():
            return jsonify({
                "error": "Please select two different countries."
            }), 400

        countries = load_country_data()

        actual_country1 = next(
            (name for name in countries if name.lower() == country1.lower()),
            None
        )

        actual_country2 = next(
            (name for name in countries if name.lower() == country2.lower()),
            None
        )

        if not actual_country1 or not actual_country2:
            return jsonify({
                "error": "One or both countries were not found."
            }), 404

        data1 = countries[actual_country1]
        data2 = countries[actual_country2]

        # Calculate vaccination percentage
        def vaccination_percentage(data):

            vaccinated = data["fully_vaccinated"]
            population = data["population"]

            if (
                vaccinated is None
                or population is None
                or population == 0
            ):
                return None

            return round((vaccinated / population) * 100, 2)

        return jsonify({

            "country1": {
                "name": actual_country1,
                "date": data1["date"],
                "total_cases": data1["cases"],
                "total_deaths": data1["deaths"],
                "fully_vaccinated": data1["fully_vaccinated"],
                "population": data1["population"],
                "cases_per_million": data1["cases_per_million"],
                "vaccination_percentage": vaccination_percentage(data1)
            },

            "country2": {
                "name": actual_country2,
                "date": data2["date"],
                "total_cases": data2["cases"],
                "total_deaths": data2["deaths"],
                "fully_vaccinated": data2["fully_vaccinated"],
                "population": data2["population"],
                "cases_per_million": data2["cases_per_million"],
                "vaccination_percentage": vaccination_percentage(data2)
            }

        })

    except Exception as error:

        print("Comparison API Error:", error)

        return jsonify({
            "error": "An error occurred while comparing countries."
        }), 500


# Run Flask application
if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )

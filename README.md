COVID-19 Trend Analysis and Visualization
Project Overview

The COVID-19 Trend Analysis and Visualization project analyzes historical COVID-19 data from different countries to understand the spread of the pandemic.

The project uses Python for data cleaning and analysis, Matplotlib for visualizations, and Flask to build an interactive web dashboard.
 Project Objectives

- Analyze COVID-19 cases and deaths across countries.
- Identify countries with the highest reported cases and deaths.
- Explore historical COVID-19 trends.
- Analyze vaccination coverage.
- Compare COVID-19 statistics between countries.
- Present important findings through an interactive dashboard.

Features

1. Dashboard Overview – Displays summary statistics from the dataset.
2. Data Insights – Identifies countries with the highest cases, deaths and vaccination coverage.
3. Country Analysis – Search and view statistics for individual countries.
4. Country Comparison – Compare statistics between two selected countries.
5. Trend Analysis – Explore historical COVID-19 cases and deaths.
6. Death Analysis – Visualizes death statistics and death rates.
7. Vaccination Analysis – Displays vaccination coverage across countries.

 Technologies Used

- Python
- Flask
- Matplotlib
- HTML
- CSS
- JavaScript
- Chart.js
- CSV

 Project Structure

```text
COVID19_Trend_Analysis/
│
├── data/
│   ├── covid_data.csv
│   └── covid_data_cleaned.csv
│
├── analysis/
│   ├── data_cleaning.py
│   ├── eda.py
│   └── trend_analysis.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
├── reports/
├── app.py
└── requirements.txt
```

 Dataset

Source: Our World in Data

Dataset link: https://ourworldindata.org/covid-cases

The dataset contains country-wise information, including:

- Confirmed COVID-19 cases
- New cases
- Total deaths
- New deaths
- Cases per million
- Deaths per million
- People vaccinated
- People fully vaccinated
- Population

 How to Run the Project

 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

 2. Open the project folder

```bash
cd COVID19_Trend_Analysis
```

 3. Install dependencies

```bash
pip install -r requirements.txt
```

 4. Run the Flask application

```bash
python app.py
```

 5. Open the dashboard

Visit:

```text
http://127.0.0.1:5000
```

 Data Cleaning and Analysis

The project performs data quality checks, handles missing country and date information, checks duplicate country-date records, and prepares a cleaned CSV file.

Missing numerical values are preserved where data is unavailable rather than automatically treated as zero.

 Important Note

The dashboard displays the latest available records for each country. Summing country-level latest cumulative values is not necessarily equivalent to an official global total because reporting dates and aggregate records can differ.

 Future Improvements

- Add interactive filters for dates and continents.
- Improve country comparison with normalized metrics.
- Add downloadable analysis reports.
- Include additional data quality visualizations.

 Author

Sivaneshwaran S.

B.Tech – Artificial Intelligence and Data Science

Data Analytics | Python | SQL | Data Visualization

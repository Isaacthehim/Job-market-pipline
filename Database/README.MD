# Iran Job Market Analysis Pipeline

End-to-end data pipeline: web scraping → SQL Server → Power BI dashboard,
analyzing job postings from jobvision.ir

## What this project does
- Scrapes live job posting data via API (Python)
- Stores and models it in a normalized SQL Server database
- Visualizes it in a 4-5 page Power BI report (salary, benefits, filters, industries)

## Architecture
![architecture](docs-architecture.png)

## Key Findings

- Sales & Marketing had the largest share of job postings in the dataset.
- More than half of the listed positions were open to both men and women.
- Employers offered 25 different types of employee benefits, with 81% of job postings including at least one benefit.
- The dataset covers job opportunities across 45 different industries.



## Dashboard preview
![overview](jobmarket-overview.png)
![salary](Salaries.png)

## Tech stack
Python · requests · SQL Server · Power BI · DAX

## Data pipeline debugging highlights

This project was built entirely by me, from start to finish. I designed the data pipeline, wrote the scraping logic, cleaned and transformed the raw API responses, designed the SQL Server schema, and built the Power BI dashboard.

One of the biggest challenges was working with the raw API data. The responses contained many fields that were unnecessary for analysis, so I identified the relevant information, extracted only the required attributes, and transformed them into a clean, structured dataset suitable for SQL Server and Power BI.

During development, I also debugged issues related to data extraction, transformation, and Power BI measures to ensure the final dashboard produced accurate and consistent results.
# GCPToLookerStudio

## Overview
GCPToLookerStudio is an Analytic Engineering project that extracts, transforms, and loads property data from various sources into Google BigQuery. The processed data is then made available for visualization and reporting in Looker Studio.

## Project Structure
- **main.py**: Core ETL logic and utility functions.
- **my_dbt_project/**: Contains dbt models, tests, and configuration for data transformation.
- **input/**: Directory for raw input files (e.g., properties_1.txt, properties_2.txt).
- **output/**: Processed data and results (if applicable).
- **.github/workflows/ci.yml**: CI/CD pipeline for automated testing and deployment.

## Data Flow
1. Raw property data is placed in the `input/` folder.
2. ETL scripts process and clean the data.
3. dbt models transform the data and load it into BigQuery (`rightmove_property` dataset).
4. The final output is stored in BigQuery and can be visualized in Looker Studio.

## Output Location
- **Google BigQuery**: Dataset `rightmove_property` in project `savvy-depot-465313-h2`.

## CI/CD
- Automated tests (pytest, dbt test) run on each push.
- Docker image is built and published to GitHub Container Registry.
- Slack notifications are sent on pipeline failures.

## Getting Started
1. Clone the repository.
2. Place raw data files in the `input/` directory.
3. Configure your dbt profile and Google Cloud credentials.
4. Run the ETL and dbt models locally or via CI/CD.

## Contact
For questions or support, please open an issue or contact the
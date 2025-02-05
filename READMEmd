# ETL Application

ETL application for processing PC and NB cost data. This application loads data from CSV files, processes them, and generates statistical reports in Excel format.

## Project Structure

```
etl-project/
├── src/
│   ├── __init__.py
│   ├── data_loader.py    # Handles CSV file loading
│   ├── data_processor.py # Implements data analysis logic
│   ├── excel_writer.py   # Handles Excel output generation
│   └── main.py          # Main ETL process
│
├── tests/
│   ├── __init__.py      # Test initialization and configuration
│   └── test_etl.py      # Comprehensive unit tests
│
├── data/
│   ├── input/           # Place input CSV files here
│   │   ├── PC.csv
│   │   └── NB.csv
│   └── output/          # Generated Excel files
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Features

- Loads and validates CSV data for PC and NB products
- Calculates statistics:
  - Maximum cost ISN across all products
  - Cost statistics (max, min, average)
  - Battery cost statistics for notebooks
- Generates Excel report with results
- Comprehensive error handling and logging
- Test coverage reporting

## Requirements

- Python 3.11+
- pandas
- openpyxl
- pytest (for testing)
- pytest-cov (for coverage reporting)

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Input File Requirements

### PC.csv columns:
- Product Type
- ISN
- Defective
- CPU Cost
- Network Card Cost
- Total Cost

### NB.csv columns (same as PC.csv plus Battery Cost):
- Product Type
- ISN
- Defective
- CPU Cost
- Network Card Cost
- Battery Cost
- Total Cost

## Usage

1. Place your input CSV files in the `data/input` directory:
   - PC.csv
   - NB.csv

2. Run the ETL process:
```bash
python src/main.py
```

3. Find the results in `data/output/result.xlsx`

## Testing

Run unit tests with unittest:
```bash
python -m unittest discover -v
```

Run basic tests with coverage report:
```bash
pytest -v --cov=src
```

Generate detailed HTML coverage report:
```bash
# Generate HTML report
pytest --cov=src --cov-report=html

# Open the report (Windows)
start htmlcov/index.html

# Open the report (Linux)
xdg-open htmlcov/index.html

# Open the report (Mac)
open htmlcov/index.html
```

The HTML report provides:
- Line-by-line coverage information
- Branch coverage analysis
- Missing lines highlighting
- Interactive source code view
- Coverage percentage by file

The test suite includes:
- Custom test result printing with pass/fail emojis
- Comprehensive test cases for all components
- Mock objects for file operations
- Exception handling verification
- Edge case testing

## Development Notes

- Column names in CSV files should match exactly (case-sensitive)
- The 'Defective ' column will be automatically stripped of trailing spaces during loading
- All cost values should be integers
- The output Excel file contains three sections:
  1. Maximum cost ISN
  2. Cost statistics
  3. Battery cost statistics (NB only)
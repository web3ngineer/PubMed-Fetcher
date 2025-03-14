# PubMed Fetcher

A command-line tool to fetch research papers from PubMed, extract metadata, and save the results as a CSV file. This tool is designed to identify non-academic authors, company affiliations, and corresponding author emails.

## Features
- Fetches research papers from PubMed using their API.
- Extracts relevant information: Title, Authors, Affiliations, Publication Date, Corresponding Author Email.
- Filters Non-Academic Authors based on affiliation keywords.
- Saves results as a CSV file.
- Debug mode for detailed logging.
- Includes automated testing using `pytest`.

---

## Installation
### Prerequisites
- Python 3.10 or above
- Poetry for dependency management
- API access to PubMed (via NCBI Entrez APIs)

### Setup
1. **Clone the Repository:**
```bash
 git clone <your-repo-url>
 cd Backend-Assignment
```

2. **Install Poetry (if not already installed):**
```bash
pip install poetry
```

3. **Install Dependencies:**
```bash
poetry install
```

4. **Create a `.env` file in the `root` directory:**
```bash
BASE_URL=https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
FETCH_URL=https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
```

---

## Usage
### CLI Tool Commands
#### Basic Usage
```bash
poetry run python cli_tool.py "<query>" <max_results> [-d] [-f <output_file.csv>] [-h]
```

#### Arguments
- `<query>`: The search term to query PubMed.
- `<max_results>`: Maximum number of results to fetch (Required).
- `-d, --debug`: Enables debug mode.
- `-f, --file`: Specifies the CSV file to save the results.
- `-h, --help`: Displays detailed help information.

#### Example Commands
```bash
# Fetch papers with debug mode enabled
poetry run python cli_tool.py "cancer research" 10 -d

# Save results to a file
poetry run python cli_tool.py "cancer research" 10 -f results.csv

# Display help information
poetry run python cli_tool.py -h
```

---

## Running Tests
Tests are located in the `tests` directory.

Run all tests using:
```bash
poetry run pytest
```

Run tests with detailed output:
```bash
poetry run pytest -v
```

---

## Project Structure
```
Backend-Assignment/
│                         # Root Directory
│── cli_tool.py           # Command-line interface tool
|       
├──pubMed_fetcher
│   ├─── fetcher.py       # Core module for fetching data
│   ├── processor.py      # Module to save data as CSV
│
├── tests/                # Test directory
│   ├── test_fetcher.py
│   └── test_processor.py
│
├── .env                  # Environment variables (in src/ directory)
├── pyproject.toml        # Poetry configuration file
└── README.md             # This file
```

---



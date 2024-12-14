# PrivateDataInteraction

**PrivateDataInteraction** is a Python library designed for handling synthetic private data interactions, providing tools for data validation, analysis, and secure data management.


**ALL DATA IS SYNTHETIC**

This project is intended for testing and demonstration purposes only. It exclusively works with synthetic data.


## Features

### 1. Data Management
- Secure handling of synthetic data
- Support for multiple data sources
- Column-level metadata management
- Data validation and sanitization

### 2. API Components
This project includes a **FastAPI backend** and a **Streamlit frontend**:
- **FastAPI Backend**:
  - Handles data validation and processing
- **Streamlit Interface**:
  - User-friendly interface for:
    - CSV file validation
    - Data analysis
    - Dataset submission with metadata

### 3. Jupyter Notebooks
A collection of Jupyter notebooks is provided for various data processing tasks:
- Icelandic age distribution processing
- Income distribution processing
- Data generation
- Research proposal examples
- Incoming data creation

## Installation

Install the library using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Usage

### Running the Streamlit App

The Streamlit app offers a web interface for interacting with the data. 

#### Features:
- **Upload and validate CSV files**
- **Analyze data contents**
- **Submit datasets with metadata**

To start the app, run:

```bash
streamlit run app.py
```

### Running the FastAPI Backend

The FastAPI backend provides an API for data validation and processing. To start the backend, run:

```bash
uvicorn main:app --reload
```

## Documentation

The documentation is built using [Sphinx](https://www.sphinx-doc.org/) and is automatically deployed to GitHub Pages when changes are pushed to the `main` or `github-documentation` branches. 

To build the documentation locally:

```bash
cd docs
make html
```

### Configuration:
- Sphinx documentation settings: `docs/conf.py`
- Dependencies: `pyproject.toml`


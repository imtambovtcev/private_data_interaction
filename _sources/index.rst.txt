PrivateDataInteraction
======================

A Python library for handling synthetic private data interactions with support for data validation, analysis, and secure data handling.

Installation
------------

Install using Poetry:

Features
--------

1. Data Management
    - Secure handling of synthetic data
    - Support for multiple data sources
    - Column-level metadata management
    - Data validation and sanitization

2. API Components
    The project includes a FastAPI backend and Streamlit frontend:
    - **FastAPI Backend**: Handles data validation and processing
    - **Streamlit Interface**: Provides a user-friendly interface for:
      - CSV file validation
      - Data analysis
      - Dataset submission

3. Jupyter Notebooks
    The project includes several Jupyter notebooks for different data processing tasks:
    - Icelandic age distribution processing
    - Income distribution processing
    - Data generation
    - Research proposal examples
    - Incoming data creation

Usage
-----

Running the Streamlit App
~~~~~~~~~~~~~~~~~~~~~~~~~

The Streamlit app provides a web interface for data interaction:

The app allows users to:
- Upload and validate CSV files
- Analyze data contents
- Submit datasets with metadata

Documentation
-------------

Build the documentation using Sphinx:

Documentation is automatically deployed to GitHub Pages when changes are pushed to `main` or `github-documentation` branches using the GitHub Actions workflow defined in `publish-sphinx-documentation.yml`.

Configuration
-------------

- Sphinx documentation configuration in `conf.py`
- Project dependencies managed in `pyproject.toml`

Note
----

As stated in `README.md`:

**ALL DATA IS SYNTHETIC**

This project only works with synthetic data for testing and demonstration purposes.
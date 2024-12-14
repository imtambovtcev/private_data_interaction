API Documentation
==================

This document describes how to interact with the API for validating, analyzing, and submitting CSV files along with their metadata.

Base URL
--------
The API is hosted locally at:

```
http://127.0.0.1:8000/
```

Endpoints
---------

### 1. Validate CSV File

**Endpoint:** `/validate-csv/`

**Method:** `POST`

**Description:** Validates the structure and content of a CSV file. Ensures all rows have a consistent number of columns.

**Input:**
- `file`: A CSV file (must have a `.csv` extension).

**Output:**
- Success: A JSON response with a success message.
- Failure: A 400 error with a detailed error message.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/validate-csv/" -F "file=@example.csv"
```

---

### 2. Analyze CSV File

**Endpoint:** `/analyze-csv/`

**Method:** `POST`

**Description:** Analyzes the structure of a CSV file and provides information about its columns and data types.

**Input:**
- `file`: A CSV file (must have a `.csv` extension).

**Output:**
- Success: A JSON response containing column names and their inferred data types.
- Failure: A 400 error with a detailed error message.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze-csv/" -F "file=@example.csv"
```

---

### 3. Submit Dataset

**Endpoint:** `/submit-dataset/`

**Method:** `POST`

**Description:** Submits a dataset (CSV file) along with its metadata (JSON file). Validates both files and checks consistency between metadata and CSV columns.

**Input:**
- `csv_file`: A CSV file (must have a `.csv` extension).
- `metadata_file`: A JSON file containing metadata about the CSV file.

**Output:**
- Success: A JSON response with details about the CSV and metadata columns.
- Failure: A 400 error with a detailed error message.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/submit-dataset/" \
-F "csv_file=@example.csv" \
-F "metadata_file=@example_metadata.json"
```

---

Validation Rules
----------------
- **CSV Validation:**
  - All rows must have the same number of columns.
  - The file must be properly encoded (auto-detected).
- **Metadata Validation:**
  - Metadata must include `dataset_name`, `description`, and `columns`.
  - Columns in the metadata must match those in the CSV file.
  - Each column in the metadata must include a `type` field.

Error Handling
--------------
- If a file fails validation, the API will return a 400 status code with a detailed error message.
- Ensure both files are properly formatted before submission.

Example Interactions
--------------------
### Validating a CSV File
```bash
curl -X POST "http://127.0.0.1:8000/validate-csv/" -F "file=@valid_dataset.csv"
```

### Analyzing a CSV File
```bash
curl -X POST "http://127.0.0.1:8000/analyze-csv/" -F "file=@valid_dataset.csv"
```

### Submitting a Dataset
```bash
curl -X POST "http://127.0.0.1:8000/submit-dataset/" \
-F "csv_file=@valid_dataset.csv" \
-F "metadata_file=@valid_metadata.json"
```
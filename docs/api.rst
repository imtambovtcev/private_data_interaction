API Documentation
====================================

This guide explains how to use the API for validating, analyzing, and submitting CSV files along with metadata. You can interact with the API in two ways:

1. **Direct HTTP requests** using tools like `curl`.
2. **Drag-and-drop** via the provided Streamlit-based user interface.

Usage Options
-------------
You can use the API endpoints directly or through a user-friendly Streamlit interface.

Drag-and-Drop Interface
-----------------------
The Streamlit-based interface provides an intuitive way to interact with the API:

1. Navigate to the UI (if hosted publicly or locally).
2. Use the drag-and-drop functionality for:
   - **CSV validation**: Upload a file and see validation results.
   - **CSV analysis**: Upload a file to get details about its structure.
   - **Dataset submission**: Upload both a CSV and metadata file.

**Example Workflow in the Interface:**

1. Open the app in your browser.
2. Select or upload your CSV file.
3. Review the results for validation, analysis, or submission.

API Endpoints
-------------
For more control or automated interaction, you can directly use the API endpoints:

### 1. Validate a CSV File
**URL:** `/validate-csv/`

**Method:** `POST`

**Purpose:** Validates the structure of the provided CSV file.

**Request:**

- **Headers:** `Content-Type: multipart/form-data`
- **Form Data:**
  - `file`: A `.csv` file.

**Response:**

- **Success (200):**

  .. code-block:: json

     {
        "detail": "CSV validation succeeded.",
        "message": "File is valid"
     }

- **Failure (400):**

  .. code-block:: json

     {
        "detail": "CSV validation failed: Inconsistent row length at row 3"
     }

**Example:**

.. code-block:: bash

   curl -X POST "http://127.0.0.1:8000/validate-csv/" -F "file=@correct_csv.csv"

---

### 2. Analyze a CSV File
**URL:** `/analyze-csv/`

**Method:** `POST`

**Purpose:** Analyzes the structure of a CSV file and provides inferred data types for each column.

**Request:**

- **Headers:** `Content-Type: multipart/form-data`
- **Form Data:**
  - `file`: A `.csv` file.

**Response:**

- **Success (200):**

  .. code-block:: json

     {
        "detail": "CSV file is valid",
        "columns": [
          {"column_name": "id", "data_type": "int64"},
          {"column_name": "name", "data_type": "object"}
        ]
     }

- **Failure (400):**

  .. code-block:: json

     {
        "detail": "Inconsistent row length at row 3"
     }

**Example:**

.. code-block:: bash

   curl -X POST "http://127.0.0.1:8000/analyze-csv/" -F "file=@correct_csv.csv"

---

### 3. Submit a Dataset
**URL:** `/submit-dataset/`

**Method:** `POST`

**Purpose:** Validates and submits a dataset (CSV file) along with its metadata (JSON file).

**Request:**

- **Headers:** `Content-Type: multipart/form-data`
- **Form Data:**
  - `csv_file`: The CSV file.
  - `metadata_file`: The metadata file in JSON format.

**Response:**

- **Success (200):**

  .. code-block:: json

     {
        "detail": "Dataset and metadata validation succeeded.",
        "csv_columns": ["id", "name"],
        "metadata_columns": ["id", "name"]
     }

- **Failure (400):**

  .. code-block:: json

     {
        "detail": "Metadata validation failed: Missing 'columns' field in metadata."
     }

**Example:**

.. code-block:: bash

   curl -X POST "http://127.0.0.1:8000/submit-dataset/" \
   -F "csv_file=@correct_csv.csv" \
   -F "metadata_file=@correct_csv_metadata.json"

---

Drag-and-Drop Example in Streamlit
-----------------------------------
When using the Streamlit-based UI, the following actions are available:

### Validating a CSV File

1. Select or upload a CSV file.
2. View the validation result, which shows whether the file is valid or contains structural issues.

### Analyzing a CSV File

1. Drag-and-drop a CSV file into the interface.
2. Review the column names and their inferred data types.

### Submitting a Dataset

1. Upload both a CSV and its metadata JSON file.
2. Receive confirmation about successful submission or errors in the files.

Error Handling
--------------
For all API endpoints, the following error codes are used:

- **400 Bad Request:** For invalid input or failed validation. The `detail` field in the response explains the issue.
- **500 Internal Server Error:** For unexpected errors during processing. Contact support with the request details if this occurs.

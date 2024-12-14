import csv
import json

import chardet
import pandas as pd
from fastapi import FastAPI, Form, HTTPException, UploadFile

app = FastAPI()


def validate_csv(file):
    """Validate the structure and content of a CSV file."""
    try:
        # Detect encoding
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        file.seek(0)
        decoded_data = raw_data.decode(encoding)

        # Check CSV structure
        csv_reader = csv.reader(decoded_data.splitlines())
        headers = next(csv_reader)  # Check headers
        column_count = len(headers)

        for line_num, row in enumerate(csv_reader, start=2):
            if len(row) != column_count:  # Check row consistency
                return False, f"Inconsistent row length at row {line_num}"
        return True, "File is valid"
    except Exception as e:
        return False, str(e)


def validate_metadata(metadata: dict, csv_columns: pd.Index) -> list:
    """Validate the metadata against the CSV columns."""
    errors = []

    # Check required metadata fields
    required_keys = ["dataset_name", "description", "columns"]
    for key in required_keys:
        if key not in metadata:
            errors.append(f"Missing required metadata field: {key}")

    # Check column definitions
    if "columns" in metadata:
        metadata_columns = metadata["columns"]
        for column_name, column_info in metadata_columns.items():
            # Ensure the column exists in the CSV
            if column_name not in csv_columns:
                errors.append(
                    f"Column '{column_name}' in metadata does not exist in CSV.")
            # Check type description exists
            if "type" not in column_info:
                errors.append(
                    f"Missing 'type' for column '{column_name}' in metadata.")
    else:
        errors.append("Missing 'columns' field in metadata.")

    # Check if metadata column count matches CSV column count
    if len(metadata.get("columns", {})) != len(csv_columns):
        errors.append(
            "Mismatch between number of columns in metadata and CSV.")

    return errors


@app.post("/validate-csv/")
async def validate_csv_endpoint(file: UploadFile):
    """
    Endpoint to validate the structure and content of a CSV file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="The file must be a CSV file.")

    try:
        # Validate the CSV file
        is_valid_csv, validation_message = validate_csv(file.file)
        if not is_valid_csv:
            raise HTTPException(
                status_code=400, detail=f"CSV validation failed: {validation_message}")
        return {"detail": "CSV validation succeeded.", "message": validation_message}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error during CSV validation: {e}")


@app.post("/submit-dataset/")
async def submit_dataset(csv_file: UploadFile, metadata_file: UploadFile):
    """
    Endpoint to validate and submit a dataset.
    Accepts a CSV file and a JSON metadata file.
    """
    # Validate file extensions
    if not csv_file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="The dataset file must be a CSV file.")
    if not metadata_file.filename.endswith(".json"):
        raise HTTPException(
            status_code=400, detail="The metadata file must be a JSON file.")

    # Validate the CSV file
    is_valid_csv, csv_message = validate_csv(csv_file.file)
    if not is_valid_csv:
        raise HTTPException(
            status_code=400, detail=f"CSV file validation failed: {csv_message}")

    # Validate the metadata file
    try:
        metadata_content = await metadata_file.read()
        metadata = json.loads(metadata_content)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid JSON format in metadata file: {e}")

    # Load the CSV with pandas
    csv_file.file.seek(0)  # Reset file pointer for pandas
    try:
        df = pd.read_csv(csv_file.file)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error reading CSV file with pandas: {e}")

    # Validate metadata against the CSV
    metadata_errors = validate_metadata(metadata, df.columns)
    if metadata_errors:
        raise HTTPException(
            status_code=400, detail=f"Metadata validation failed: {', '.join(metadata_errors)}")

    return {
        "detail": "Dataset and metadata validation succeeded.",
        "csv_columns": list(df.columns),
        "metadata_columns": list(metadata.get("columns", {}).keys())
    }


@app.post("/analyze-csv/")
async def analyze_csv_file(file: UploadFile):
    """Endpoint to analyze a CSV file."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Only CSV files are allowed.")

    # Validate the file
    is_valid, message = validate_csv(file.file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    # Use pandas to infer column names and types
    try:
        file.file.seek(0)  # Reset file pointer after validation
        df = pd.read_csv(file.file)
        column_info = [{"column_name": col, "data_type": str(
            df[col].dtype)} for col in df.columns]
        return {
            "detail": "CSV file is valid",
            "columns": column_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}")

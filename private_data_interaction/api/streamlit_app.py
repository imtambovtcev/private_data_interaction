import streamlit as st
import requests
import os

# Define API endpoints
VALIDATE_API_URL = "http://127.0.0.1:8000/validate-csv/"
ANALYZE_API_URL = "http://127.0.0.1:8000/analyze-csv/"
SUBMIT_DATASET_API_URL = "http://127.0.0.1:8000/submit-dataset/"

PREDEFINED_PAIRS = {
    'Income Dataset': {
        'csv': os.path.abspath('../test_upload_data/hagstofa_data.csv'),
        'metadata': os.path.abspath('../test_upload_data/hagstofa_metadata.json')
    },
    'Medical Dataset': {
        'csv': os.path.abspath('../test_upload_data/medical_data.csv'),
        'metadata': os.path.abspath('../test_upload_data/medical_metadata.json')
    },
    "Correct Dataset": {
        "csv": os.path.abspath("../test_upload_data/correct_csv.csv"),
        "metadata": os.path.abspath("../test_upload_data/correct_csv_metadata.json")
    },
    "Incorrect Dataset": {
        "csv": os.path.abspath("../test_upload_data/incorrect_csv.csv"),
        "metadata": os.path.abspath("../test_upload_data/incorrect_csv_metadata.json")
    },

}


def validate_file_via_api(file_path):
    """Send the file to the validation API."""
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                VALIDATE_API_URL,
                files={"file": (os.path.basename(file_path), f)}
            )
        if response.status_code == 200:
            return True, response.json().get("detail", "File is valid!")
        else:
            return False, response.json().get("detail", "Error in file validation.")
    except Exception as e:
        return False, str(e)


def analyze_file_via_api(file_path):
    """Send the file to the analysis API."""
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                ANALYZE_API_URL,
                files={"file": (os.path.basename(file_path), f)}
            )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Error in file analysis.")
    except Exception as e:
        return False, str(e)


def submit_dataset_via_api(csv_path, metadata_path):
    """Send the dataset and metadata to the submission API."""
    try:
        with open(csv_path, "rb") as csv_file, open(metadata_path, "rb") as metadata_file:
            response = requests.post(
                SUBMIT_DATASET_API_URL,
                files={
                    "csv_file": (os.path.basename(csv_path), csv_file),
                    "metadata_file": (os.path.basename(metadata_path), metadata_file)
                }
            )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Error in dataset submission.")
    except Exception as e:
        return False, str(e)


# Streamlit UI
st.title("CSV Validator, Analyzer, and Dataset Submission")

# Validator Section
st.subheader("Validate a CSV File")
# Dropdown for predefined files
validate_file_option = st.selectbox(
    "Select a file to validate:", list(PREDEFINED_PAIRS.keys()), key="validator")
if st.button("Validate Selected File"):
    file_path = PREDEFINED_PAIRS[validate_file_option]["csv"]
    is_valid, message = validate_file_via_api(file_path)
    st.write("Validation Result:")
    if is_valid:
        st.success(message)
    else:
        st.error(message)

# Drag-and-drop for validation
validate_uploaded_file = st.file_uploader(
    "Or upload a CSV file to validate:", type=["csv"], key="validate_upload")
if validate_uploaded_file:
    st.write(f"Uploaded file: {validate_uploaded_file.name}")
    temp_path = "temp_validate_uploaded_file.csv"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(validate_uploaded_file.getbuffer())

    is_valid, message = validate_file_via_api(temp_path)
    st.write("Validation Result:")
    if is_valid:
        st.success(message)
    else:
        st.error(message)

    # Cleanup
    os.remove(temp_path)

# Analyzer Section
st.subheader("Analyze a CSV File")
# Dropdown for predefined files
analyze_file_option = st.selectbox(
    "Select a file to analyze:", list(PREDEFINED_PAIRS.keys()), key="analyzer")
if st.button("Analyze Selected File"):
    file_path = PREDEFINED_PAIRS[analyze_file_option]["csv"]
    is_valid, result = analyze_file_via_api(file_path)
    st.write("Analysis Result:")
    if is_valid:
        st.success(result["detail"])
        st.write("Columns:")
        for col in result["columns"]:
            st.write(f"- {col['column_name']} ({col['data_type']})")
    else:
        st.error(result)

# Drag-and-drop for analysis
analyze_uploaded_file = st.file_uploader(
    "Or upload a CSV file to analyze:", type=["csv"], key="analyze_upload")
if analyze_uploaded_file:
    st.write(f"Uploaded file: {analyze_uploaded_file.name}")
    temp_path = "temp_analyze_uploaded_file.csv"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(analyze_uploaded_file.getbuffer())

    is_valid, result = analyze_file_via_api(temp_path)
    st.write("Analysis Result:")
    if is_valid:
        st.success(result["detail"])
        st.write("Columns:")
        for col in result["columns"]:
            st.write(f"- {col['column_name']} ({col['data_type']})")
    else:
        st.error(result)

    # Cleanup
    os.remove(temp_path)

# Submit Dataset Section
st.subheader("Submit a Dataset")
# Dropdown for predefined dataset-metadata pairs
submit_pair_option = st.selectbox(
    "Select a dataset-metadata pair to submit:", list(PREDEFINED_PAIRS.keys()), key="submit_pair")
if st.button("Submit Selected Pair"):
    csv_path = PREDEFINED_PAIRS[submit_pair_option]["csv"]
    metadata_path = PREDEFINED_PAIRS[submit_pair_option]["metadata"]
    is_valid, result = submit_dataset_via_api(csv_path, metadata_path)
    st.write("Submission Result:")
    if is_valid:
        st.success(result["detail"])
        st.write("CSV Columns:", result["csv_columns"])
        st.write("Metadata Columns:", result["metadata_columns"])
    else:
        st.error(result)

# Drag-and-drop for dataset submission
st.write("Or upload a dataset and its metadata for submission:")
uploaded_csv = st.file_uploader("Upload CSV file:", type=[
                                "csv"], key="dataset_csv")
uploaded_metadata = st.file_uploader("Upload Metadata file:", type=[
                                     "json"], key="dataset_metadata")

if uploaded_csv and uploaded_metadata:
    st.write(f"Uploaded CSV file: {uploaded_csv.name}")
    st.write(f"Uploaded Metadata file: {uploaded_metadata.name}")
    temp_csv_path = "temp_uploaded_dataset.csv"
    temp_metadata_path = "temp_uploaded_metadata.json"

    with open(temp_csv_path, "wb") as temp_csv_file:
        temp_csv_file.write(uploaded_csv.getbuffer())
    with open(temp_metadata_path, "wb") as temp_metadata_file:
        temp_metadata_file.write(uploaded_metadata.getbuffer())

    is_valid, result = submit_dataset_via_api(
        temp_csv_path, temp_metadata_path)
    st.write("Submission Result:")
    if is_valid:
        st.success(result["detail"])
        st.write("CSV Columns:", result["csv_columns"])
        st.write("Metadata Columns:", result["metadata_columns"])
    else:
        st.error(result)

    # Cleanup
    os.remove(temp_csv_path)
    os.remove(temp_metadata_path)

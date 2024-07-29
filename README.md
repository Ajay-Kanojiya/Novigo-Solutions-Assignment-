# Novigo Solutions Assignment

A FastAPI API that accepts form data, fills out the fields in a provided PDF form and returns a PDF.

    Requirements:

        - Use the provided sample_pdf.pdf form.
        - Fill the form with the supplied data.
        - Return the filled PDF as a response.

## Prerequisites:

- Python3
- FastAPI
- fillpdf
- Uvicorn

## Installation Steps:

1. Install Python if it is not present in system
    ```sh
   sudo apt update
   sudo apt install python3

2. Verify Python Installation:
    ```sh
    python3 --version

## Steps to run the project:

3. Clone the repository:
    ```sh
    git clone https://github.com/Ajay-Kanojiya/Novigo-Solutions-Assignment-.git

4. Install dependencies:
    ```sh
    pip3 install -r requirements.txt

5. Run app

    ```sh
    python3 novigo_app.py

6. Navigate to swagger docs
    ```sh
    http://127.0.0.1:8060/docs

7. Test the API endpoint by uploading ```sample_pdf.pdf```
    * Endpoint: ```http://127.0.0.1:8060/fillpdf```
    * Method: ```POST```





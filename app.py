from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from google.api_core.exceptions import InvalidArgument
import os

from utils import get_gemini_response, input_image_setup, extract_pdfs_from_zip, format_response

# Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadInvoice', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"})
    
    files = request.files.getlist('files')
    
    file_bytes_list = []
    file_names = []
    for uploaded_file in files:
        if uploaded_file.filename == '':
            continue
        file_name = uploaded_file.filename
        file_names.append(file_name)
        if uploaded_file and uploaded_file.filename.endswith('.zip'):
            # Extract PDFs from the zip file
            file_bytes_list.extend([(pdf_bytes, "application/pdf", file_name) for pdf_bytes in extract_pdfs_from_zip(uploaded_file)])
        else:
            file_bytes_list.append((uploaded_file.read(), uploaded_file.mimetype, file_name))
    
    responses = []
    for file_bytes, file_type, file_name in file_bytes_list:
        image_data, images = input_image_setup(file_bytes, file_type)
        input_prompt= """
            You are an expert in understanding invoices. You will receive input images as invoices.
            Please extract the following details from the invoice:
            - Invoice Number
            - Bill To
            - Ship Address
            - Date
            - Total Amount
            - Order ID
        """
        try:
            response = get_gemini_response(image_data[0], input_prompt)
            formatted_response = format_response(response, file_name)
            responses.append(formatted_response)
        except InvalidArgument as e:
            return jsonify({"error": "Error processing file", "details": str(e)})
    
    return render_template('result.html', responses=responses)

if __name__ == '__main__':
    app.run(debug=True)

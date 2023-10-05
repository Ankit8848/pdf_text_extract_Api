from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import base64
import os

app = Flask(__name__)


@app.route('/extract_text', methods=['POST'])
def extract_text_from_pdf():
    try:
        # Get the PDF data from the request JSON
        data = request.get_json()
        pdf_data_base64 = data.get('data')

        if not pdf_data_base64:
            return jsonify({'error': 'Missing PDF data in request JSON'}), 400

        # Decode the base64-encoded PDF data
        pdf_data = base64.b64decode(pdf_data_base64)

        # Open the PDF using PyMuPDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        # Initialize the extracted text variable
        extracted_text = ""

        # Iterate through each page and extract text
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            extracted_text += page.get_text()

        # Close the PDF document
        pdf_document.close()

        # Prepare the response JSON object
        response_data = {
            'data': extracted_text
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=True)

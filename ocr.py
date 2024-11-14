from flask import Flask, jsonify, request
from flask_cors import CORS
import easyocr
import os
import tempfile  # Import tempfile module

app = Flask(__name__)
CORS(app)  
port = 9000

@app.route('/')
def home():
    return jsonify({'status': 'OCR BACKEND 2 IS RUNNING'})

@app.route('/scrap', methods=['POST'])
def scrap_portfolio():
    try:
        # Ensure an image file is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files.get("image")

        # Create a temporary file using tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file_path = temp_file.name  # Get the temporary file path
            image_file.save(temp_file_path)  # Save the uploaded file to the temp path

        # Use EasyOCR to read the text from the image
        reader = easyocr.Reader(['en'])
        result = reader.readtext(temp_file_path, detail=0)

        # Optionally, delete the temporary file
        os.remove(temp_file_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrap', methods=['GET'])
def scrap_folder():
    try:
        # Get folder path from query parameters
        folder_path = 'C:/Users/jaink/Pictures/Screenshots'
        if not folder_path or not os.path.isdir(folder_path):
            return jsonify({'error': 'Invalid or missing folder path'}), 400
        
        # Initialize an array to store OCR results for each image
        ocr_results = []

        # Iterate over PNG files in the specified folder
        for file_name in os.listdir(folder_path):
            print(file_name)
            if file_name.lower().endswith('.png'):
                file_path = os.path.join(folder_path, file_name)

                # Use EasyOCR to read the text from the image
                reader = easyocr.Reader(['en'])
                result = reader.readtext(file_path, detail=0)
                
                # Store the result along with the file name for reference
                ocr_results.append({'file_name': file_name, 'text': result})

        return jsonify(ocr_results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)




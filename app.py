from flask import Flask, render_template_string, request
import os
import html
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/<file_name>', methods=['GET'])
def home(file_name='file1.txt'):
    # Dictionary to store file content
    file_content = {}
    
    # List of files to read
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
    
    # Check if the requested file exists
    if file_name not in files:
        return render_error_page('File not found!')
    
    # List of encodings to try
    encodings = ['utf-8', 'utf-16', 'gbk']
    
    # Attempt to read the file with different encodings
    for encoding in encodings:
        try:
            # Read content of the requested file
            with open(file_name, 'r', encoding=encoding) as f:
                file_content = f.read()
            break  # Stop trying encodings if successful
        except Exception as e:
            pass  # Try next encoding
    
    # Check if file content is empty
    if not file_content:
        return render_error_page('Error reading file: Unsupported encoding or file is empty.')
    
    # Get start and end line numbers from query parameters
    start_line = int(request.args.get('start', 1))
    end_line_param = request.args.get('end', None)
    
    if end_line_param is not None:
        end_line = int(end_line_param)
    else:
        end_line = None
    
    # Split the content into lines
    lines = file_content.split('\n')
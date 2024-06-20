from flask import render_template, request
from app.llm_gemini_extract.gemini_extract import extract_data

def info_extract():
    if request.method == 'POST':
        data = request.get_json()
        input_text = data.get('input_text')
        result = extract_data(input_text)

        # Return dataset shape and head as JSON
        return result
    
    return render_template('llm_generate.html')
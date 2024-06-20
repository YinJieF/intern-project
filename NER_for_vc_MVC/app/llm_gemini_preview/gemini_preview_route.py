from flask import render_template, request, jsonify

from app.llm_gemini_preview.gemini_dataset_preview import load_data

def g_data_preview():
    if request.method == 'POST':
        table_id = "criminal_data_gemini"
        project_id = 'intern-project-415606'
        selected_dataset = 'Criminal_Dataset'

        # Load data using provided parameters
        data_html, dataset_shape = load_data(project_id, selected_dataset, table_id)
        
        return jsonify(data_html=data_html, dataset_shape=dataset_shape)

    # If it's a GET request, render the data.html template
    return render_template('llm_preview.html')
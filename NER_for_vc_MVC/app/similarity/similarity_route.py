from flask import render_template, request, jsonify
from app.similarity.find_similarity import read_bq, find_top_similar

def similarity_compare():
    if request.method == 'POST':
        data = request.get_json()
        input_name, compare_type, num = data.get('input_name'), data.get('compare_type'), data.get('resultNum')
        table_id = "criminal_name_vector"
        project_id = 'intern-project-415606'
        selected_dataset = 'Criminal_Dataset'

        # Load data using provided parameters
        df = read_bq(project_id, selected_dataset, table_id)
        
        # find the top similar
        result_html = find_top_similar(df, input_name, compare_type, num)

        # Return dataset shape and head as JSON
        return jsonify(result_html=result_html)
    
    return render_template('similarity.html')
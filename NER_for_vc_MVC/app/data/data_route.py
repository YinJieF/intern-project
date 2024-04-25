from flask import render_template, request, jsonify

from app.data.preview_data import get_bq_tables, load_data, data_description

def data_inspect():
    if request.method == 'POST':
        data = request.json
        dataset_size, table_id  = data.get('datasetSize'), data.get('dataset')
        table_id = "criminal_data_inorder"
        project_id = 'intern-project-415606'
        selected_dataset = 'Criminal_Dataset'

        # Load data using provided parameters
        df = load_data(project_id, selected_dataset, table_id, int(dataset_size))
        
        data_html, dataset_shape= data_description(df)
        
        percentage = ['10', '17', '16', '13', '13', '13 ']
        # Return dataset shape and head as JSON
        return jsonify(percentage=percentage, data_html=data_html, dataset_shape=dataset_shape)
    
    # If it's a GET request, render the data.html template
    datasets = get_bq_tables('Criminal_Dataset')  # Replace 'your_dataset_id_here' with your actual dataset ID
    return render_template('data.html', datasets=datasets)

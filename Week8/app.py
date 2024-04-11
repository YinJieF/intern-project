from train import training
from flask import Flask, request, jsonify, render_template
from data_inspect import get_bq_tables, load_data, data_description
from record_train import get_training_info, add_record_begin, add_record_done

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.json
        dataset_size, table_id  = data.get('datasetSize'), data.get('dataset')

        project_id = 'intern-project-415606'
        selected_dataset = 'Criminal_Dataset'

        # Load data using provided parameters
        df = load_data(project_id, selected_dataset, table_id, int(dataset_size))
        
        dataset_shape, dataset_head, dataset_columns = data_description(df)
        
        # Return dataset shape and head as JSON
        return jsonify(dataset_shape=dataset_shape, dataset_head=dataset_head, dataset_columns=dataset_columns)
    
    # If it's a GET request, render the data.html template
    datasets = get_bq_tables('Criminal_Dataset')  # Replace 'your_dataset_id_here' with your actual dataset ID
    return render_template('data.html', datasets=datasets)

@app.route('/train', methods=['GET', 'POST'])
def train_page():
    if request.method == 'POST':
        data = request.json
        table_id, dataset_size, model = data.get('dataset'), data.get('datasetSize'), data.get('model')

        if model == 'NERModel':
            job_uuid = add_record_begin(table_id, dataset_size) 
            filepath_model, filepath_result = training(table_id, int(dataset_size))
            add_record_done(job_uuid, filepath_model, filepath_result)
            get_training_info()
            return jsonify(train_info=get_training_info())  # Return updated training information as JSON
        
    return render_template('train.html', datasets=get_bq_tables('Criminal_Dataset'), training_info=get_training_info())

if __name__ == '__main__':
    app.run(debug=True)     
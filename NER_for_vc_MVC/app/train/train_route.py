from flask import render_template, request, jsonify
from app.data.preview_data import get_bq_tables
from app.train.record_train import get_training_info
from app.train.model_train import training

def model_training():
    if request.method == 'POST':
        data = request.json
        table_id, dataset_size, model_selection = data.get('dataset'), data.get('datasetSize'), data.get('model')

        training(table_id, int(dataset_size))

        get_training_info()
        return jsonify(train_info=get_training_info())  # Return updated training information as JSON
        
    return render_template('train.html', datasets=get_bq_tables('Criminal_Dataset'), training_info=get_training_info())

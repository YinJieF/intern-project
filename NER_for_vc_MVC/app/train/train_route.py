from flask import render_template, request, jsonify
from app.data.preview_data import get_bq_tables
from app.train.record_train import get_training_info
from app.train.model_train import training

def model_training():
    if request.method == 'POST':
        data = request.json
        table_id, dataset_size, model_selection = data.get('dataset'), data.get('datasetSize'), data.get('model')
        print('training...')
        training(table_id, int(dataset_size))
        get_training_info()
        train_info, train_html = get_training_info()
        return jsonify(train_info=train_info, train_html=train_html)  # Return updated training information as JSON

    train_info, train_html = get_training_info()    
    return render_template('train.html', datasets=get_bq_tables('Criminal_Dataset'), train_info=train_info, train_html=train_html)  

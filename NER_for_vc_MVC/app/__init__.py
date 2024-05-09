from flask import Flask
from app.routes import index, model_monitor
from app.data.data_route import data_inspect
from app.train.train_route import model_training
from app.inference.inference_route import model_inference
from app.similarity.similarity_route import similarity_compare

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', '/', index)
    app.add_url_rule('/data', '/data', data_inspect, methods=['GET', 'POST'])
    app.add_url_rule('/train', '/train', model_training, methods=['GET', 'POST'])
    app.add_url_rule('/inference', '/inference', model_inference, methods=['GET', 'POST'])
    app.add_url_rule('/similarity', '/similarity', similarity_compare, methods=['GET', 'POST'])
    app.add_url_rule('/monitor', '/monitor', model_monitor)

    return app
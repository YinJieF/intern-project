from flask import Flask
from app.routes import index
from app.data.data_route import data_inspect
from app.train.train_route import model_training
from app.inference.inference_route import model_inference
from app.similarity.similarity_route import similarity_compare
from app.llm_gemini_extract.gemini_extract_route import info_extract
from app.llm_gemini_preview.gemini_preview_route import g_data_preview
from app.llm_gemini_compare.gemini_compare_route import info_compare

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', '/', index)
    app.add_url_rule('/data', '/data', data_inspect, methods=['GET', 'POST'])
    app.add_url_rule('/train', '/train', model_training, methods=['GET', 'POST'])
    app.add_url_rule('/inference', '/inference', model_inference, methods=['GET', 'POST'])
    app.add_url_rule('/similarity', '/similarity', similarity_compare, methods=['GET', 'POST'])
    app.add_url_rule('/llm_generate', '/llm_generate', info_extract, methods=['GET', 'POST'])
    app.add_url_rule('/llm_dataset', '/llm_dataset', g_data_preview, methods=['GET', 'POST'])
    app.add_url_rule('/llm_similarity', '/llm_similarity', info_compare, methods=['GET', 'POST'])

    return app
from flask import Flask
from app.credit_risk_report.render_page import render_page
from app.credit_risk_report.comparison_route import compare_route
from app.credit_risk_report.risk_report_route import report_generate

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', '/', render_page, methods=['GET'])
    app.add_url_rule('/criminal_search', '/criminal_search', compare_route, methods=['GET', 'POST'])
    app.add_url_rule('/report_generate', '/report_generate', report_generate, methods=['GET', 'POST'])

    return app
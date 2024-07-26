import re
from flask import request, jsonify
from app.credit_risk_report.risk_report import get_risk_report

def report_generate():
    if request.method == 'POST':
        data = request.get_json()
        
        # check identical result
        if data['identical_results'] != []:
            name = data['identical_results'][0]['name']
            jlr_link_html= data['identical_results'][0]['jlr_link']
            url_match = re.search(r'href="([^"]+)"', jlr_link_html)
            print(name, url_match.group(1))

            risk_report = get_risk_report(name, url_match.group(1))
            print(risk_report)
            return jsonify(risk_report=risk_report)

from flask import render_template, request, jsonify
from app.llm_gemini_compare.gemini_compare import comparison

def info_compare():
    if request.method == 'POST':
        data = request.get_json()
        input_data = {
            "person": {
                "name": data.get('personName'),
                "birthdate": data.get('personBirthdate'),
                "company_name": data.get('personCompany'), 
                "province_name": data.get('personProvince'),
                "district_name": data.get('personDistrict'),
                "full_address": data.get('personAddress')
            }
        }

        result = comparison(input_data)
        identical_result, similar_result = result['identical'], result['top_5_similar']
        # Return dataset shape and head as JSON
        return jsonify(identical_result=identical_result, similar_result=similar_result)
    
    return render_template('llm_comparison.html')
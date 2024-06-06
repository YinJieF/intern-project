from flask import Flask, request, jsonify, render_template
from llama_llm import process_text
from save_llama_llm_result import save_result
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def llama_llm():
    if request.method == 'POST':
        input_text = request.json.get('input_text')
        if input_text:
            result = process_text(input_text)
            return jsonify({"result": result})
        else:
            return jsonify({"error": "input_text is required"})
    else:
        return render_template('llama_llm.html')

@app.route('/save_result', methods=['POST'])
def save():
    status = request.json.get('status')
    input_text = request.json.get('input_text')
    output_text = request.json.get('output_text')
    start_time = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')

    print(save_result(input_text, output_text, status, start_time))

    return jsonify({"saving to bq": "done"})

if __name__ == "__main__":
    app.run(debug=True)
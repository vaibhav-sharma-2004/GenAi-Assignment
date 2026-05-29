from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Module 7 Assignment API Running!"})

@app.route('/run-extraction')
def run_extraction():
    result = subprocess.run(['python', 'task5_data_extraction.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
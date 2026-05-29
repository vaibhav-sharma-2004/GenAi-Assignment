from flask import Flask, jsonify, request
import subprocess
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Task4_data_query'))
from Task4_data_query.app import load_document, ask_question

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Module 7 Assignment API Running!",
        "routes": {
            "/run-llm-chat": "Runs task2_LLM_chat.py",
            "/run-augmentation": "Runs task3_data_augmentation.py",
            "/run-extraction": "Runs task5_data_extraction.py",
            "/ask-document (POST)": "Task4 - Ask question from PDF/DOCX"
        }
    })

@app.route('/run-llm-chat')
def run_llm_chat():
    result = subprocess.run(['python', 'task2_LLM_chat.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "errors": result.stderr})

@app.route('/run-augmentation')
def run_augmentation():
    result = subprocess.run(['python', 'task3_data_augmentation.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "errors": result.stderr})

@app.route('/run-extraction')
def run_extraction():
    result = subprocess.run(['python', 'task5_data_extraction.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "errors": result.stderr})

@app.route('/ask-document', methods=['POST'])
def ask_document():
    try:
        # Check if file and question are provided
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        if 'question' not in request.form:
            return jsonify({"error": "No question provided"}), 400

        file = request.files['file']
        question = request.form['question']

        # Validate file type
        if not (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
            return jsonify({"error": "Only PDF and DOCX files are supported"}), 400

        # Save file temporarily
        temp_path = os.path.join('Task4_data_query', file.filename)
        file.save(temp_path)

        # Load document and ask question
        document_text = load_document(temp_path)
        answer = ask_question(document_text, question)

        # Remove temp file
        os.remove(temp_path)

        return jsonify({
            "file": file.filename,
            "question": question,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
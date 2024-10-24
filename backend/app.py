from flask import Flask, request, jsonify
from transformers import pipeline
import sqlite3
import spacy
import matplotlib.pyplot as PLT
import pandas as PD
import os

from parsers.pdf_parser import extract_from_pdf
from parsers.excel_parser import extract_from_excel
from parsers.word_parser import extract_from_word


#DATABASE DO NOT REMOVE 
database_path = "extracted_data.db"
conn = sqlite3.connect(database_path, check_same_thread=False)
cursor = conn.cursor()
nlp = spacy.load("en_core_web_sm")  
qa_pipeline = pipeline("question-answering")
summarizer = pipeline("summarization")


cursor.execute("""
               CREATE TABLE IF NOT EXISTS data_store (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   key TEXT,
                   value TEXT
               )
""")

conn.commit()

# INITIAL SAM FOUNDATION
app = Flask(__name__)
summarizer = pipeline("summarization")

@app.route("/process-file", methods=["POST"])
def process_file():
    file = request.files["file"]
    file_type = file.filename.split(".")[-1].lower()
    
    if file_type == "pdf":
        extracted_text = extract_from_pdf(file)
    elif file_type == "xlsx":
        extracted_text == extract_from_excel(file)
    elif file_type == "docx":
        extracted_text == extract_from_word(file)
    else:
        return jsonify({"error": "unsupported file type"}), 400

    cursor.execute("INSERT INTO data_store (key, value) VALUES (?, ?)", (file.filename, extracted_text))
    conn.commit()
    return jsonify({"message": "File processed and data stored."})

@app.route("/ask-question", methods=["POST"])
def ask_question():
    question = request.form.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    cursor.execute("SELECT value FROM data_store")
    rows = cursor.fetchall()
    
    context = " ".join([row[0] for row in rows])
    
    if not context:
         return jsonify({"error": "No data available to answer the question"}), 400
    try:
        result = qa_pipeline(question=question, context=context)
        return jsonify({"answer": result['answer'], "confidence": result['score']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
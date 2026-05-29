import os
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from docx import Document

# Load API Key
load_dotenv()

# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# READ PDF
def read_pdf(file_path):
    text = ""

    pdf = PdfReader(file_path)

    for page in pdf.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


# READ DOCX
def read_docx(file_path):
    doc = Document(file_path)

    text = "\n".join([para.text for para in doc.paragraphs])

    return text


# LOAD DOCUMENT
def load_document(file_path):

    if file_path.endswith(".pdf"):
        return read_pdf(file_path)

    elif file_path.endswith(".docx"):
        return read_docx(file_path)

    else:
        raise Exception("Unsupported file format")


# ASK QUESTION
def ask_question(document_text, question):

    prompt = f"""
You are a document assistant.

Answer ONLY from the provided document.

If the answer is not available in the document,
say:
'I could not find this information in the document.'

DOCUMENT:
{document_text}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    file_path = input("Enter document path: ")

    document_text = load_document(file_path)

    print("\nDocument Loaded Successfully\n")

    while True:

        question = input("Ask Question (type exit to quit): ")

        if question.lower() == "exit":
            break

        answer = ask_question(document_text, question)

        print("\nAnswer:")
        print(answer)
        print("\n" + "-"*50 + "\n")
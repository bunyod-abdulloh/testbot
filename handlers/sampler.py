import PyPDF2

from loader import db

#
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with open(pdf_path, "rb") as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         # for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[7]
#         text += page.extract_text()
#     return text
#
#
# test = []
#
# pdf_path = "Test Master.pdf"
# extracted_text = extract_text_from_pdf(pdf_path)
# test.append(extracted_text)
# List of questions and options
mevalar = ["1. Olma", "2. Gilos", "30. Behi", "320. O'rik", "5. Uzum"]



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
# Berilgan son
from datetime import datetime

# Berilgan vaqt
vaqt_str = "0:00:20.744321"

# Vaqt obyekti sifatida o'qish
vaqt = datetime.strptime(vaqt_str, "%H:%M:%S.%f")

# Vaqtni sekundga aylantirish
sekundlar = vaqt.hour * 3600 + vaqt.minute * 60 + vaqt.second + vaqt.microsecond / 1000000
butun_son = round(sekundlar)
print(butun_son)



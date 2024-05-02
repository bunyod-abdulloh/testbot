import PyPDF2


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        # for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[7]
        text += page.extract_text()
    return text


test = []

pdf_path = "Test Master.pdf"
extracted_text = extract_text_from_pdf(pdf_path)
test.append(extracted_text)

all_questions_data = test[0].split('\n\n')
a_2 = all_questions_data[0].split("\n")
print(a_2)
# print(all_questions_data)
questions = []
# a_zero = []
# a_str = str()
# all_questions_data = test[0].split('\n\n')
# questions = []
# c = 0
# for question_data in all_questions_data:
#     c += 1
#     print(c)
#     print(question_data)
    # questions.append(question_data.split('\n')[0])
# print(questions)


for index, question_data in enumerate(all_questions_data):

    start_index = question_data.index(f'1.')
    end_index = question_data.index(f'\nA)')
#         a_one = question_data.index('A)')
#         a_two = question_data.index('B)')
#         a_zero.append(question_data[a_one:a_two])
#         a_str = a_zero[0].split('A) ')[1]
    print(end_index)
    # for n in range(45):
    questions.append(question_data[start_index:end_index])
print(questions)
#
# print(questions)
# print(a_str)
# print(len(all_questions_data))


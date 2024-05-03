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
savols = ['1. Hello, what ______ your name?\nA) is B) are C) am D) be\n2. ______ name is John. And my ______ is '
          'Johnson.\nA) Your / surname B) My / surname\nC) I / surname D) I / name\n3. My name is Lisa. ______ Lisa '
          'Peterson.\nA) My am B) I is C) I am D) I\n4. ______ name is Apple. ______ Ann Apple.\nA) His / She B) His '
          '/ He’s C) Her / She’s D) His / His\n5. “Where ______ John from?” “______ from the US.”\nA) is / He’s B) is '
          '/ His C) am / He’s D) is / She’s\n6. ______ are you from? Japan.\nA) What B) Who C) Where D) When\n7. '
          'Where ______ you ______ ?\nA) is / from B) are / in C) are / is D) are / from\n8. ______ from Spain. I’m '
          'Rodriguez .\nA) I’m B) He’s C) You’re D) She’s\n9. Pierre is a French boy. ______ from ______ .\nA) He’s / '
          'France B) His’s / French\nC) His / France D) He / France\n10. Lisa and Max are Americans. ______ from '
          'U.S.A.\nA) There B) Their C) They’re D) Their’re\n11. “What ____ their _____?”\n“Alexander and '
          'Philip.”\nA) are/name B) is / name C) is / names D) are / names\n12. I ______ 22 years old, but Andrew '
          '______ 20.\nA) am / am B) are / am C) am / is D) are / are\n13. Mark______ 19, but Brian and Denis ______ '
          '26 and 28.\nA) is / are B) are / is C) are / are D) am / are\n14. “What ______ this?”\n“It’s ______ '
          'umbrella.”\nA) are / a B) is / a C) is / an D) its / an\n15. Oxford is ______ English university.\nA) an '
          'B) the C) a D) *\n16. Toyotas ______ Japanese ______ .\nA) is a / car B) is / car C) are / cars D) is / '
          'cars\n17. “What is ______ ?”\n“She is a bank manager.”\nA) his job B)she job C) he job D) her job\n18. '
          '0/2/11/18/20 Find the correct alternative.\nA) oh / twelve / eighteen / twenty\nB) zero / two / one-one / '
          'eighteen / twenty\nC) zero / two / eleven / eighteen / twenty\nD) zero / two / eleven / eighty / '
          'twenty\n19. “How old is your aunt?”\n“______ is 29.”\nA) She B) He C) She’s D) He’s\n20. “Where ______ she '
          'from?”\n“She ______ from Japan.”\nA) are / is B) is / is C) is / am D) are / are\n21. This ______ my '
          'friend. ______ name’s Richard.\nA) are / His B) is / My C) is / His D) his / His\n22. They ______ Lisa and '
          'Max. They ______ from the USA.\nA) is / is B) are / is C) are / are D) is / is\n23. “What is ______ name?” '
          '“My name’s Carlos.”\nA) his B) her C) your D) my\n24. This is my sister. ______ name is Laura.\nA) His B) '
          'My C) Her D) Its\n25. I have ______ brother. ______ name is David\nA) an / His B) a / Her C) a / His D) * '
          '/ His\n26. Hello! My ___ ___ Maria. I ___ ___ Mexico.\nA) name is / from am B) is name / from am\nC) name '
          'is / am from D) name am / is from\n27. Is Catherine ______ sister?\nA) he B) you C) your D) yours\n28. We '
          '______ students.\nA) are a B) is C) are D) am\n29. I ______ student.\nA) is / an B) am / * C) am / a D) am '
          '/ the\n30. She ______ Italy.\nA) are from B) is at C) is from D) am from\n31. He is ______ teacher.\nA) a '
          'B) an C) * D) the\n32. I live ______ a house ______ Los Angeles.\nA) * / in B) in / in C) in / * D) at / '
          'in\n33. “______ is your phone number?”\n“It’s 2229"\nA) Where B) How C) What D) Who\n34. “______ are '
          'you?”\n“I’m Alex.”\nA) Which B) How C) What D) Who\n35. What’s this ______ English?\nA) * B) in C) at D) '
          'on\n36. Champaigne is ______ French drink.\nA) a B) the C) an D) *\n37. Oxford is ______ English '
          'university.\nA) a B) an C) the D) *\n38. A Mercedes is ______ German car.\nA) a B) an C) the D) *\n39. '
          'English is ______ international language.\nA) a B) an C) the D) *\n40. Milan is ______ Italian city.\nA) a '
          'B) an C) the D) *\n41. A JVC is ______ Japanese camera.\nA) a B) an C) the D) *\n42. I have two ______ '
          '.\nA) sister B) sisters C) a sister D) sister’s\n43. It’s ______ Spanish orange.\nA) a B) an C) the D) '
          '*\n44. It’s ______ green apple.\nA) a B) an C) the D) *']

replace_a = savols[0].replace('”\n“', '" "')
replace_b = replace_a.replace('\nC)', ' C)')
questions_list = replace_b.split("\n")

questions_only = [question for i, question in enumerate(questions_list) if i % 2 == 0]

option = [question for i, question in enumerate(questions_list) if i % 2 == 1]

letters = ['A', 'B', 'C', 'C', 'A', 'C', 'D', 'A', 'A', 'C', 'D', 'C', 'A', 'C', 'A', 'C', 'D', 'C', 'C', 'B', 'C', 'C',
           'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'A', 'B', 'C', 'D', 'B', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'A']

savol_javob = []
for savol, togri_javob, variantlar in zip(questions_only, letters, option):
    savol_javob.append((savol, togri_javob, variantlar))

for i in savol_javob:
    print(i[0])

# for key, value in savol_javob:
#     if key == "A":
#         a_ = value.split("A)")
#         a_correct = a_[1].split("B)")[0]
#         b_ = value.split("B)")
#         b = b_[1].split("C)")[0]
#         c_ = value.split("C)")
#         c = c_[1].split("D)")[0]
#         d = value.split("D)")[1]
#         print(d)

    # split_ = key.split(f"{value})")[1]
    # print(split_)
# correct_answers = []
# for question in questions:
#   parts = question.split("?")  # Split question and answer choices
#   correct_answers.append(parts[1].split("“")[1].strip())  # Extract correct answer
#
# print(correct_answers)
#
# questions_only = []
# for question in questions:
#   questions_only.append(question.split("?")[0].strip())  # Extract question text
#
# print(questions_only)

# savollar = questions[::2]
# javoblar = questions[1::2]
# a = [1, 2, 3, 4, 5, 6]
# for item in a:
#     if item % 2 != 0:
#         print(item)

# royxat = ['apple', 'banana', 'cherry', 'date']
#
# for indeks in range(1, len(questions), 2):
#     print(f"Toq indeks: {indeks}, Qiymat: {questions[indeks]}")
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


# for index, question_data in enumerate(all_questions_data):
#
#     start_index = question_data.index(f'1.')
#     end_index = question_data.index(f'\nA)')
# #         a_one = question_data.index('A)')
# #         a_two = question_data.index('B)')
# #         a_zero.append(question_data[a_one:a_two])
# #         a_str = a_zero[0].split('A) ')[1]
#     print(end_index)
#     # for n in range(45):
#     questions.append(question_data[start_index:end_index])
# print(questions)
#
# print(questions)
# print(a_str)
# print(len(all_questions_data))

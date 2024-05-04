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


javobs = ["1-A 2-B 3-C 4-C 5-A 6-C 7-D 8-A\n9-A 10-C 11-D 12-C 13-A 14-C 15-A 16-C\n17-D 18-C 19-C 20-B 21-C 22-C 23-C "
          "24-C\n25-C 26-C 27-C 28-C 29-C 30-C 31-A 32-B\n33-C 34-D 35-B 36-A 37-B 38-A 39-B 40-B\n41-A 42-B 43-A 44-A"]



async def test_qoshish(savollar: list, kitob_nomi: str, kalit_javoblar: list):
    savol = savollar[0].replace("\nB)", " B)").replace("\nC)", " C)").replace("\nD)", " D)").replace('”\n“', '" "')
    tayyor_savollar = savol.split("\n")

    savollar = [question for i, question in enumerate(tayyor_savollar) if i % 2 == 0]

    javoblar = [question for i, question in enumerate(tayyor_savollar) if i % 2 == 1]

    answers = kalit_javoblar[0].split()

    # Harflar uchun yangi ro'yxat
    togri_javoblar = []

    # Javoblar ro'yxatidan harflarni ajratish
    for answer in answers:
        letter = answer.split('-')[1]
        togri_javoblar.append(letter)

    savol_javob = []
    for savol, togri_javob, variantlar in zip(savollar, togri_javoblar, javoblar):
        savol_javob.append((savol, togri_javob, variantlar))

    count = 0

    for savol, togri_javob, variantlar in savol_javob:
        if togri_javob == "A":
            a_ = variantlar.split("A)")
            t_javob = a_[1].split("B)")[0].lstrip()
            b_ = variantlar.split("B)")
            b = b_[1].split("C)")[0].lstrip()
            c_ = variantlar.split("C)")
            c = c_[1].split("D)")[0].lstrip()
            d = variantlar.split("D)")[1].lstrip()
            await db.add_question(
                table_name=kitob_nomi, question=savol,
                a_correct=t_javob, b=b, c=c, d=d
            )

        if togri_javob == "B":
            a_ = variantlar.split("A)")
            a = a_[1].split("B)")[0].lstrip()
            b_ = variantlar.split("B)")
            t_javob = b_[1].split("C)")[0].lstrip()
            c_ = variantlar.split("C)")
            c = c_[1].split("D)")[0].lstrip()
            d = variantlar.split("D)")[1].lstrip()
        #
        if togri_javob == "C":
            a_ = variantlar.split("A)")
            a = a_[1].split("B)")[0].lstrip()
            b_ = variantlar.split("B)")
            b = b_[1].split("C)")[0].lstrip()
            c_ = variantlar.split("C)")
            t_javob = c_[1].split("D)")[0].lstrip()
            d = variantlar.split("D)")[0].lstrip()

        if togri_javob == "D":
            a_ = variantlar.split("A)")
            a = a_[1].split("B)")[0].lstrip()
            b_ = variantlar.split("B)")
            b = b_[1].split("C)")[0].lstrip()
            c_ = variantlar.split("C)")
            c = c_[1].split("D)")[0].lstrip()
            t_javob = variantlar.split("D)")[1].lstrip()

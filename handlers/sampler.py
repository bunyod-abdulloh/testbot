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


def raqamni_ochir(matn):
    if matn[2].isdigit() and matn[3] == '.':
        matn = matn[5:]
    if matn[1].isdigit() and matn[2] == '.':
        matn = matn[4:]
    if matn[0].isdigit() and matn[1] == '.':
        matn = matn[3:]
    return matn


async def test_qoshish(savollar: list, kitob_nomi: str, kalit_javoblar: list):
    savol = savollar[0].replace("\nB)", " B)").replace("\nC)", " C)").replace("\nD)", " D)").replace('”\n“', '" "')
    tayyor_savollar = savol.split("\n")

    savollar_ = [question for i, question in enumerate(tayyor_savollar) if i % 2 == 0]
    raqamsiz_savollar = []
    for n in savollar_:
        raqamsiz_savollar.append(raqamni_ochir(n))

    javoblar = [question for i, question in enumerate(tayyor_savollar) if i % 2 == 1]

    answers = kalit_javoblar[0].split()

    # Harflar uchun yangi ro'yxat
    togri_javoblar = []

    # Javoblar ro'yxatidan harflarni ajratish
    for answer in answers:
        letter = answer.split('-')[1]
        togri_javoblar.append(letter)

    savol_javob = []
    for savol, togri_javob, variantlar in zip(raqamsiz_savollar, togri_javoblar, javoblar):
        savol_javob.append((savol, togri_javob, variantlar))

    count = 0

    for savol, togri_javob, variantlar in savol_javob:
        count += 1
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
            await db.add_question(
                table_name=kitob_nomi, question=savol,
                a_correct=t_javob, b=a, c=c, d=d
            )

        if togri_javob == "C":
            a_ = variantlar.split("A)")
            a = a_[1].split("B)")[0].lstrip()
            b_ = variantlar.split("B)")
            b = b_[1].split("C)")[0].lstrip()
            c_ = variantlar.split("C)")
            t_javob = c_[1].split("D)")[0].lstrip()
            d = variantlar.split("D)")[1].lstrip()
            await db.add_question(
                table_name=kitob_nomi, question=savol,
                a_correct=t_javob, b=b, c=a, d=d
            )

        if togri_javob == "D":
            a_ = variantlar.split("A)")
            a = a_[1].split("B)")[0].lstrip()
            b_ = variantlar.split("B)")
            b = b_[1].split("C)")[0].lstrip()
            c_ = variantlar.split("C)")
            c = c_[1].split("D)")[0].lstrip()
            t_javob = variantlar.split("D)")[1].lstrip()
            await db.add_question(
                table_name=kitob_nomi, question=savol,
                a_correct=t_javob, b=b, c=c, d=a
            )
    return count

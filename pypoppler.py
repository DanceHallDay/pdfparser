from pdfparser.cpp.build.pdf2text import PDF

pdf = PDF("/home/nktrn/Downloads/CV+Nikita+Aparovich.pdf")
pn = pdf.get_page_number()
print(pn)
td = pdf.get_text_data()
print(td[5].fontname)

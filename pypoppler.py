from pdfparser.pdf2text import PDF

pdf = PDF("/home/nktrn/Downloads/CV+Nikita+Aparovich.pdf")
pn = pdf.get_page_number()
print(pn)
td = pdf.get_text_data()
print(td[0].width)
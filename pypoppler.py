from pdfparser.cpp.build.pdf2text import PDF

pdf = PDF("/home/nktrn/Downloads/CV+Nikita+Aparovich.pdf")
pn = pdf.get_page_number()

td = pdf.get_text_data()
i = 128
a = pdf.render_word(
    td[i].page,
    td[i].x,
    td[i].y,
    td[i].width,
    td[i].height,
)
for b in a:
    print(b)

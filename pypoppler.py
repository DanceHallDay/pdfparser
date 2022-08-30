import pdfparser.pdf2text as p
import numpy as np
from PIL import Image
import io

#pdf =p.PDF("/home/nktrn/Downloads/CV+Nikita+Aparovich.pdf")
pdf =p.PDF("/home/nktrn/Downloads/test.pdf")

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
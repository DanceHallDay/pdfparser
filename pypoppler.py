import pdfparser.pdf2text as p2t

a = p2t.get_text_data("pdf path")
a = " ".join([str(i.text) for i in a])
"""
other attributes:
x
y
width
height
page
"""
print(a)
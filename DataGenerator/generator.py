from PIL import Image, ImageDraw, ImageFont


def render_word(txt):
    font = ImageFont.truetype('fonts/Yacimiento ExtraBold Ex.ttf', size=42)
    l, t, r, b = font.getbbox(txt)
    w, h = r - l, b - t

    image = Image.new("RGBA", (w, h), (255,255,255))
    draw = ImageDraw.Draw(image)
    draw.text((-l, -t), txt, (0,0,0), font=font)
    image.save("img.png")


render_word("word")
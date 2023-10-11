from ia.gpt import make_history
from ia.stability import generate_image
import os
from PIL import ImageDraw, ImageFont
import textwrap

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

about = "Uma criança que gostava de jogar futebol"

history_sentences = make_history(about)
history_sentences.insert(0, about)

total_sentences = len(history_sentences)

img_width = 512
img_height = 512

pdf_width = img_width / mm * 2.83464567
pdf_height = img_height / mm * 2.83464567

output_path = f'./output/{about}'

if not os.path.exists(output_path):
    os.mkdir(output_path)

pdf = canvas.Canvas(f'{output_path}/{about}.pdf', pagesize=(pdf_width, pdf_height))

for sentence_index, sentence in enumerate(history_sentences):
    print(f'{sentence_index} of {total_sentences}')
    img = generate_image(about, sentence, img_width, img_height)

    width, height = img.size

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("./font/Schoolbell-Regular.ttf", 24)

    border_width = 3

    max_width = img_width - 80

    text_lines = textwrap.wrap(sentence, width=max_width // font.getsize('x')[0])

    y = -40
    total_lines = len(text_lines)

    for line_index, line in enumerate(text_lines):

        w, h = draw.textsize(line, font=font)
        text_pos = ((width - w) / 2, (height - h))

        if line_index == 0:
            y += (height - (h * total_lines))

        draw.text((text_pos[0], y), line, font=font, fill='white', stroke_width=border_width, stroke_fill='black')
        y += font.getsize(line)[1]

    img.save(f'{output_path}/{sentence_index}.jpg')
    pdf.drawInlineImage(img, 0, 0)
    pdf.showPage()

pdf.save()


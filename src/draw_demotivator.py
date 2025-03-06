from PIL import Image, ImageDraw, ImageFont
import io

def make_dem(img, text, ttf="arial.ttf"):

    black_border = 40
    white_border = 1
    font_size = 60
    line_spacing = 10 # addition between lines

    image = Image.open(io.BytesIO(img))
    width, height = image.size
    
    l_width = width + 2 
    l_heigth = height + 2
    light_frame = Image.new("RGB", (l_width, l_heigth), "white")
    light_frame.paste(image, (1, 1))
    draw = ImageDraw.Draw(light_frame)

    bf_width = l_width + 2 * black_border 
    bf_height = l_heigth + 2 * black_border + 150 # Extra space below
    black_framed = Image.new("RGB", (bf_width, bf_height), "black")
    black_framed.paste(light_frame, (black_border, black_border))
    draw = ImageDraw.Draw(black_framed)
    
    try:
        font = ImageFont.truetype(ttf, font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "Sample", font=font)
    line_height = bbox[3] - bbox[1]  # Height of a single line
    text_y = height + 2 * black_border - 20

    lines = text.split("\n")
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (bf_width - text_width) // 2
        draw.text((text_x, text_y), line, font=font, fill="white")
        text_y += line_height + line_spacing

    wf_width = bf_width + 2 * white_border
    wf_height = bf_height + 2 * white_border
    white_framed = Image.new("RGB", (wf_width, wf_height), "white")
    white_framed.paste(black_framed, (white_border, white_border))
    draw = ImageDraw.Draw(black_framed)

    out = io.BytesIO()
    white_framed.save(out, format='PNG')
    out.seek(0)

    return out

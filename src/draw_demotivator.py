from PIL import Image, ImageDraw, ImageFont
import io

def make_dem(img, text, ttf="arial.ttf"):

    image = Image.open(io.BytesIO(img))
    width, height = image.size

    longer_part = width
    if height > width:
        longer_part = height
    black_border = longer_part // 15
    white_border = 1
    font_size = (height + width) // 24
    line_spacing = font_size // 6 # extra space between lines

    
    # create white 1px frame
    l_width = width + 2 
    l_height = height + 2
    light_frame = Image.new("RGB", (l_width, l_height), "white")
    light_frame.paste(image, (1, 1))
    draw = ImageDraw.Draw(light_frame)

    # create black frame
    bf_width = l_width + 2 * black_border 
    bf_height = l_height + 2 * black_border + int(longer_part // 5) # Extra space below
    black_framed = Image.new("RGB", (bf_width, bf_height), "black")
    black_framed.paste(light_frame, (black_border, black_border))
    draw = ImageDraw.Draw(black_framed)
    
    font = ImageFont.truetype(ttf, font_size)

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
        # add more space between lines
        text_y += line_height + line_spacing
        # change second line size
        font_size = int(font_size * 0.7)
        font = ImageFont.truetype(ttf, font_size)

    wf_width = bf_width + 2 * white_border
    wf_height = bf_height + 2 * white_border
    white_framed = Image.new("RGB", (wf_width, wf_height), "white")
    white_framed.paste(black_framed, (white_border, white_border))
    draw = ImageDraw.Draw(black_framed)

    out = io.BytesIO()
    white_framed.save(out, format='PNG')
    out.seek(0)

    return out

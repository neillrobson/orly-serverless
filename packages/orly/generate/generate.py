import os, re, datetime
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont


def generate_image(
    title,
    topText,
    author,
    image_code,
    theme,
    guide_text_placement="bottom_right",
    guide_text="The Definitive Guide",
):
    themeColors = {
        "0": (85, 19, 93, 255),
        "1": (113, 112, 110, 255),
        "2": (128, 27, 42, 255),
        "3": (184, 7, 33, 255),
        "4": (101, 22, 28, 255),
        "5": (80, 61, 189, 255),
        "6": (225, 17, 5, 255),
        "7": (6, 123, 176, 255),
        "8": (247, 181, 0, 255),
        "9": (0, 15, 118, 255),
        "10": (168, 0, 155, 255),
        "11": (0, 132, 69, 255),
        "12": (0, 153, 157, 255),
        "13": (1, 66, 132, 255),
        "14": (177, 0, 52, 255),
        "15": (55, 142, 25, 255),
        "16": (133, 152, 0, 255),
    }
    themeColor = themeColors[theme]

    width = 500
    height = 700
    im = Image.new("RGBA", (width, height), "white")

    font_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "fonts", "Garamond Light.ttf")
    )
    font_path_helv = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "fonts", "HelveticaNeue-Medium.otf")
    )
    font_path_helv_bold = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "fonts", "Helvetica Bold.ttf")
    )
    font_path_italic = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "fonts", "Garamond LightItalic.ttf")
    )

    topFont = ImageFont.truetype(font_path_italic, 20)
    subtitleFont = ImageFont.truetype(font_path_italic, 34)
    authorFont = ImageFont.truetype(font_path_italic, 24)
    titleFont = ImageFont.truetype(font_path, 62)
    oriellyFont = ImageFont.truetype(font_path_helv, 28)
    questionMarkFont = ImageFont.truetype(font_path_helv_bold, 16)

    dr = ImageDraw.Draw(im)
    dr.rectangle(((20, 0), (width - 20, 10)), fill=themeColor)

    topText = sanitize_unicode(topText, font_path_italic)
    _, _, textWidth, textHeight = dr.textbbox((0, 0), topText, topFont)
    textPositionX = (width / 2) - (textWidth / 2)

    dr.text((textPositionX, 10), topText, fill="black", font=topFont)

    author = sanitize_unicode(author, font_path_italic)
    _, _, textWidth, textHeight = dr.textbbox((0, 0), author, authorFont)
    textPositionX = width - textWidth - 20
    textPositionY = height - textHeight - 20

    dr.text((textPositionX, textPositionY), author, fill="black", font=authorFont)

    oreillyText = "O RLY"

    _, _, textWidth, textHeight = dr.textbbox((0, 0), oreillyText, oriellyFont)
    textPositionX = 20
    textPositionY = height - textHeight - 20

    dr.text((textPositionX, textPositionY), oreillyText, fill="black", font=oriellyFont)

    oreillyText = "?"

    textPositionX = textPositionX + textWidth

    dr.text(
        (textPositionX, textPositionY - 1),
        oreillyText,
        fill=themeColor,
        font=questionMarkFont,
    )

    titleFont, newTitle = clamp_title_text(
        sanitize_unicode(title, font_path), width - 80
    )
    if newTitle == None:
        raise ValueError("Title too long")

    _, _, textWidth, textHeight = dr.multiline_textbbox((0, 0), newTitle, titleFont)
    dr.rectangle([(20, 400), (width - 20, 400 + textHeight + 40)], fill=themeColor)

    subtitle = sanitize_unicode(guide_text, font_path_italic)

    if guide_text_placement == "top_left":
        _, _, textWidth, textHeight = dr.textbbox((0, 0), subtitle, subtitleFont)
        textPositionX = 20
        textPositionY = 400 - textHeight - 2
    elif guide_text_placement == "top_right":
        _, _, textWidth, textHeight = dr.textbbox((0, 0), subtitle, subtitleFont)
        textPositionX = width - 20 - textWidth
        textPositionY = 400 - textHeight - 2
    elif guide_text_placement == "bottom_left":
        textPositionY = 400 + textHeight + 40
        _, _, textWidth, textHeight = dr.textbbox((0, 0), subtitle, subtitleFont)
        textPositionX = 20
    else:  # bottom_right is default
        textPositionY = 400 + textHeight + 40
        _, _, textWidth, textHeight = dr.textbbox((0, 0), subtitle, subtitleFont)
        textPositionX = width - 20 - textWidth

    dr.text((textPositionX, textPositionY), subtitle, fill="black", font=subtitleFont)

    dr.multiline_text((40, 420), newTitle, fill="white", font=titleFont)

    cover_image_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "images", ("%s.png" % image_code))
    )
    coverImage = Image.open(cover_image_path).convert("RGBA")

    offset = (80, 40)
    im.paste(coverImage, offset, coverImage)

    final_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ("%s.png" % datetime.datetime.now()))
    )
    im.save(final_path)

    im.close()

    return final_path


def clamp_title_text(title, width):
    im = Image.new("RGBA", (500, 500), "white")
    dr = ImageDraw.Draw(im)

    font_path_italic = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "fonts", "Garamond Light.ttf")
    )
    # try and fit title on one line
    font = None

    startFontSize = 80
    endFontSize = 61

    for fontSize in range(startFontSize, endFontSize, -1):
        font = ImageFont.truetype(font_path_italic, fontSize)
        _, _, w, h = dr.textbbox((0, 0), title, font)

        if w < width:
            return font, title

    # try and fit title on two lines
    startFontSize = 80
    endFontSize = 34

    for fontSize in range(startFontSize, endFontSize, -1):
        font = ImageFont.truetype(font_path_italic, fontSize)

        for match in list(re.finditer("\s", title, re.UNICODE)):
            newTitle = "".join(
                (title[: match.start()], "\n", title[(match.start() + 1) :])
            )
            _, _, substringWidth, h = dr.multiline_textbbox((0, 0), newTitle, font)

            if substringWidth < width:
                return font, newTitle

    im.close()

    return None, None


def sanitize_unicode(string, font_file_path):
    sanitized_string = ""

    font = TTFont(font_file_path)
    cmap = font["cmap"].getcmap(3, 1).cmap
    for char in string:
        code_point = ord(char)

        if code_point in list(cmap.keys()):
            sanitized_string = str.join("", (sanitized_string, char))

    return sanitized_string

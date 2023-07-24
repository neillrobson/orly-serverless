from generate import generate_image


def main(event):
    title = event.get("title", "Title Text Goes Here")
    topText = event.get("top_text", "This is where top text goes")
    author = event.get("author", "Kanstantsin Tsedryk")
    image_code = event.get("image_code", "7")
    theme = event.get("theme", "3")
    guide_text_placement = event.get("guide_text_placement", "bottom_right")
    guide_text = event.get("guide_text", "The Definitive Guide")

    png = generate_image(
        title, topText, author, image_code, theme, guide_text_placement, guide_text
    )

    return {
        "headers": {"Content-Type": "image/png"},
        "statusCode": 200,
        "body": png.decode(),
    }

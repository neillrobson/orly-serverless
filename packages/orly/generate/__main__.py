from generate import generate_image


def main(event):
    title = event.get("title", "Title Goes Here")
    topText = event.get("top_text", "This is top text.")
    author = event.get("author", "Kanye West")
    image_code = event.get("image_code", "2")
    theme = event.get("theme", "1")
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

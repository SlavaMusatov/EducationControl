from PIL import Image, ImageDraw
from random import randint

def new_color():
    red = randint(100, 200)
    green = randint(100, 200)
    blue = randint(100, 200)
    return (red, green, blue)

def generate_picture():
    color1 = new_color()
    new_image = Image.new('RGB', (300, 400), new_color())
    draw = ImageDraw.Draw(new_image)

    draw.ellipse((50, 50, 250, 250), outline = color1, width=10, fill=new_color())
    draw.ellipse((100, 100, 130, 130), fill=color1, width=0)
    draw.ellipse((170, 100, 200, 130), fill = color1, width=0)

    draw.line((100, 190, 130, 200), fill = color1, width=10)
    draw.line((130, 200, 170, 200), fill=color1, width=10)
    draw.line((170, 200, 200, 190), fill=color1, width=10)

    draw.rectangle((50, 270, 250, 500), outline=color1, width=10, fill = new_color())

    return new_image



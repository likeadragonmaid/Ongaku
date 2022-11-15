import subprocess
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageSequence


def neofetch():
    neofetch = subprocess.run(
        "neofetch --stdout", shell=True, capture_output=True
    ).stdout.decode("utf-8")
    if len(neofetch) == 0:
        return
    neo_ = neofetch.split("\n")
    x, y = 125, 150
    gf = Image.open("ongaku/resources/images/neofetch_template.gif")
    frames = []
    font_ = ImageFont.truetype("ongaku/resources/NotoSans-Regular.ttf", 50)
    count = 1
    text_ = "Ongaku is running \n"
    for frame in ImageSequence.Iterator(gf):
        try:
            text_ += f"{neo_[count]}\n"
        except IndexError:
            pass
        draw = ImageDraw.Draw(frame)
        draw.text(xy=(x, y), text=text_, font=font_, fill="white")
        pic = BytesIO()
        frame.save(pic, format="GIF")
        frame = Image.open(pic)
        frames.append(frame)
        count += 1
    n_gif = BytesIO()
    frames[0].save(n_gif, save_all=True, append_images=frames[1:], format="GIF")
    n_gif.name = "neofetch.gif"
    # frames[0].save("neofetch.gif", save_all=True, append_images=frames[1:])
    return n_gif

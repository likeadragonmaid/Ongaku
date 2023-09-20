"""

 * neofetch.py: File to generate neofetch gif for Ongaku

  Copyright (C) 2023 likeadragonmaid, Ryuk

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""

from io import BytesIO

try:
    from PIL import Image, ImageDraw, ImageFont, ImageSequence

    pil_installed = True
except ModuleNotFoundError:
    pil_installed = False


def neofetch(neo):
    if not pil_installed:
        return "pil not installed"
    neo_ = neo.split("\n")
    x, y = 100, 25
    gif_ = Image.open("ongaku/resources/images/neofetch_template.gif")
    frames = []
    font_ = ImageFont.truetype("ongaku/resources/NotoSans-Regular.ttf", 23)
    count = 1
    text_ = "Ongaku is running \n"
    for frame in ImageSequence.Iterator(gif_):
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
    #neo_gif = BytesIO()
    #frames[0].save(neo_gif, save_all=True, append_images=frames[1:], format="GIF")
    #neo_gif.name = "neofetch.gif"
    frames[0].save("neofetch.gif", save_all=True, append_images=frames[1:], format="GIF")
    return 

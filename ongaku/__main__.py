"""

 * __main__.py: Main file for Ongaku

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

import logging

from ongaku.looper import loop_, reset_bio

from ongaku import ongaku

logging.basicConfig(level=logging.ERROR)


async def boot():
    # importlib.import_module("bot.plugins.commands")
    await loop_()


if __name__ == "__main__":
    try:
        ongaku.start()
        ongaku.run(boot())
    except KeyboardInterrupt:
        ongaku.run(reset_bio(restart=False))
        print("\nOngaku: Stopped")

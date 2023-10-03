"""

 * create_client.py: File to authenticate Ongaku with a telegram account

  Copyright (C) 2022 Shouko

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

import os

from pyrogram import Client

if os.path.isfile("TG_SESSION.session"):
    os.remove("TG_SESSION.session")

a_id = os.environ.get("API_ID", 0)
a_hash = os.environ.get("API_HASH", 0)


def generate_session():
    API_ID = int(a_id) or int(input("Enter API_ID: "))
    API_HASH = a_hash or input("Enter API_HASH: ")
    with Client("TG_SESSION", api_id=API_ID, api_hash=API_HASH, in_memory=True) as app:
        session = app.export_session_string()
        app.send_message("me", f"#STRING_SESSION\n\n`{session}`")
        print(
            f"#Session \n\n{session}\n\nexported to your saved messages\nPlease add it to config.env"
        )

if __name__=="__main__":
    generate_session()
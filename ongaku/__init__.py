import os
import sys

from dotenv import load_dotenv
from ongaku.tools.create_client import generate_session

if not load_dotenv("config.env"):
    print("config.env Not found.")
    sys.exit()

print("Ongaku: config.env Loaded")

for var in {"API_ID", "API_HASH", "USERS", "LOOP"}:
    if not os.environ.get(var):
        print(f"Required {var} var.")
        sys.exit()

print("Ongaku: Checking Session")

if not os.environ.get("STRING_SESSION"):
    print("Ongaku: Starting for the first time")
    generate_session()
    print("Please Add the session to your config.env and run the project again.")
    sys.exit()

print("Ongaku: Session Found")

if int(os.environ.get("LOOP", 0)):
    print(
        """Ongaku: Bot is set to work until manually stopped.
        It can be stopped by Ctrl+C or killing the process(s)
"""
    )
else:
    print(
        """Ongaku: Bot is set to stop if there is no music notification.
        You can change this behavior.
"""
    )

from ongaku.config import Config
from .core.client import Ongaku

ongaku = Ongaku()

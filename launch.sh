#!/bin/bash

echo "Ongaku: Checking for updates"
git fetch && git pull
source venv/bin/activate

if [ $termux -eq 1 ]; then
	echo -e "Termux: Acquiring wakelock"
	termux-wake-lock
fi

python3 -m ongaku
deactivate

if [ $termux -eq 1 ]; then
	echo -e "Termux: Releasing wakelock"
	termux-wake-unlock
fi

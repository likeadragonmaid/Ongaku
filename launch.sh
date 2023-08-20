#!/bin/bash

check_vars() {
  for var in API_ID API_HASH USERS LOOP; do
      test -z ${!var} && echo -e "\nRequired $var var !"
  done
  if [ -z "${MUSIC_PLAYER}" ] && [ "${NOW_PLAYING_PIXEL_MODE}" != "true" ]; then
      echo -e "\nRequired MUSIC_PLAYER var or NOW_PLAYING_PIXEL_MODE set to true !" && exit
fi
}

checksession() {
  if test $STRING_SESSION; then
     echo "Ongaku: Session found"
  else
     echo "Ongaku: Starting for the first time"
     python3 ongaku/create_client.py
     echo "Please check for session in your saved messages in telegram. Add it to your config.env and run the project again."
     exit
  fi
}


checkconfig() {
  if test -f "config.env"; then
     export $(grep '^[A-Z].*' config.env | xargs)
     echo -e "Ongaku: config.env loaded\nOngaku: Checking session"
  else
     echo "Please add API_ID AND API_HASH in config.env"
     exit
  fi
}


checkTermuxEnv() {
if [ $(uname -o) == "Android" ]; then
	termux=1
	if [ -z $(getprop ro.miui.ui.version.name) ]; then
        	miui=0
	else
        	miui=1
		echo -e "Termux: MIUI device detected\nTermux: Ongaku is unsupported!\nTermux: Please check README.md for more details"
	fi
fi
}

#updateRemote() {
#if [ $(git config --get remote.origin.url) == "https://github.com/gibcheesepuffs/ongaku" ]; then
#	git remote set-url origin https://github.com/Ongaku-TG/ongaku.git
#fi
#}

#updateRemote
echo "Ongaku: Checking for updates"
git fetch && git pull
source venv/bin/activate
checkconfig
checksession
check_vars
checkTermuxEnv

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

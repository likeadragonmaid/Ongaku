#!/bin/bash

check_vars() {
  for var in API_ID API_HASH USERS MUSIC_PLAYER LOOP; do
      test -z ${!var} && echo -e "\nRequired $var var !" && exit
  done
}

checksession() {
  if test $STRING_SESSION; then
     echo "
Ongaku: Session found"
  else
     echo "
Ongaku: Starting for the first time"
     python3 create_client.py
     echo "
Please check for session in your saved messages in telegram. Add it to your config.env and run the project again."
     exit
  fi
}


checkconfig() {
  if test -f "config.env"; then
     export $(grep '^[A-Z].*' config.env | xargs)
     echo -e "
Ongaku: config.env loaded\n\nOngaku: Checking session"
  else
     echo "Please add API_ID AND API_HASH in config.env"
     exit
  fi
}


checkTermuxEnv() {
if [ $(uname -o) == "Android" ]; then
	termux=1
fi
}


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

python3 main.py
deactivate

if [ $termux -eq 1 ]; then
	echo -e "Termux: Releasing wakelock"
	termux-wake-unlock
fi

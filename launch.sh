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


echo "Ongaku: Checking for updates"
git fetch && git pull
source venv/bin/activate
checkconfig
checksession
check_vars
export PYTHONWARNINGS="ignore::DeprecationWarning"
python3 main.py
deactivate

<p align="center"><img src="https://raw.githubusercontent.com/Ongaku-TG/ongaku/main/ongaku/resources/images/logos/ongaku-logo_github.png"></p>
A **smol and fluffy** telegram bot to update your bio with music playing on your android phone in real time!

### Requirements
* An android device capable of running Termux
* A music player app capable of showing notifications of current music being played
### Getting started

* Install [Termux](https://f-droid.org/en/packages/com.termux/) and [Termux:API](https://f-droid.org/en/packages/com.termux.api/) apps from F-Droid.
* Launch Termux and run the following commands

```
apt update && apt dist-upgrade -y && apt update && apt install -y git nano python python-pip termux-api && git clone https://github.com/Ongaku-TG/ongaku && cd ongaku && pip install virtualenv && virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && deactivate && cd .. && termux-notification-list
```

Optionally you can also add neofetch support by running

```
apt install -y libjpeg-turbo libxcb libraqm libimagequant openjpeg tcl libtiff littlecms freetype neofetch && source venv/bin/activate && pip install -r requirements-optional.txt && deactivate
```

You will be asked to provide notification access to Termux:API app. You must provide Termux:API app all the required permissions. You may be required to do `Ctrl+C` to continue.

* When you run the Ongaku for the first time you are asked to enter your phone number to create a session. Ongaku uses this session to work with your telegram account.

* Create a `config.env` file from `sample-config.env`

$ `cd ongaku && cp sample-config.env config.env`

Edit `config.env` as instructed by the file itself.

$ `nano config.env`

* You can get `API_ID` and `API_HASH` from [here](https://my.telegram.org/).

* You can use this [app](https://f-droid.org/en/packages/com.oF2pks.applicationsinfo/) to check package name of your music player app and add it to `MUSIC_PLAYER` value.

* To optionally get `LOG_CHANNEL` create a private telegram channel and send a random message in it. After that forward that message to [@username_to_id_bot](https://t.me/username_to_id_bot) on telegram or [here](https://t.me/username_to_id_bot).

* You can leave out `STRING_SESSION` for now by uncommenting it.

* Starting [IDBot](https://t.me/username_to_id_bot) on telegram will also give you your own ID. Put that in `USERS` value.

Use `Ctrl+X` to exit and save your changes.

* Run `./launch` inside the root `ongaku` directory. You will receive your `STRING_SESSION` in your saved messages in telegram app.

* Copy the session text and edit your `config.env` file once again by running `nano config.env`

* Paste your session text according to the instructions in the file.

Use `Ctrl+X` to exit and save your changes.

* Run `./launch` inside `ongaku` directory once again.

* If this is your first time launching Ongaku then you will be asked to enter your phone number to login. Next launches will work without having to re-login.

* If everything went well you should be up and running. At this point you can start playing music and you should see current playing song in the Termux app and in the telegram channel you set for logging if any.

### Tips

* Ongaku may stop detecting notifications and responding to commands if you `RELEASE WAKELOCK` while it is running! It handles android wakelocks automatically.
* If you frequently switch between multiple music players, you may want to keep multiple `config.env` files. You can make any number of `.env` files named like `config-1.env, config-2.env, config-3.env...` and so on. To keep any one the file active at one time, you just have to rename that file to `config.env` and use launch script as usual.

### Known Limitations

* Ongaku cannot yet differentiate between the states of music player itself i.e. `Playing`, `Paused` and `Stopped`. It simply assumes existing music player notification as a `Playing` state.
* It is not yet possible to run Ongaku on a baremetal server or a VPS/PaaS such as Heroku.
* Devices running MIUI are unsupported as Xiaomi loves to corrupt notification permission after X amount of hours and even at each device reboot. However you can still use Ongaku if you are willing to provide notification access manually by uninstalling Termux:API app, reinstalling it again, running `termux-notification-list` and lastly doing `Ctrl + C` each time Ongaku starts malfunctioning! This is something you can also fix by running a reputable custom rom such as [LineageOS](https://lineageos.org/). (**#RipBozo** 💯🤣🤣 if you choose to run MIUI on your phone anyway)

### Optional commands
Send in any telegram chat

`.about` to view info about the project.

`.history` to get list of music played in current session.

`.sync` to force sync bio with latest notification.

`.alive` to get environment information in GIF format (not actual mp4 video with no audio scam format).

`.alive -t` to get environment information in text format.

### Authors
* [Shouko](https://github.com/gibcheesepuffs)
* [Ryuk](https://github.com/anonymousx97)

### Support
[Shouko's Lab](https://t.me/shoukolab)

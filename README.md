# Ongaku

A **smol and fluffy** telegram bot to update your bio with music playing on your android phone in real time!

### Requirements

* An android device capable of running Termux
* A music player app capable of showing notifications of current music being played
* The package name of your music player app, you can use [this](https://f-droid.org/en/packages/com.oF2pks.applicationsinfo/) app to check package name of your app

### Getting started

* Install [Termux](https://f-droid.org/en/packages/com.termux/) and [Termux:API](https://f-droid.org/en/packages/com.termux.api/) apps from F-Droid.
* Launch Termux and run the following commands

```
apt update && apt dist-upgrade -y && apt install -y git nano python termux-api && git clone https://github.com/gibcheesepuffs/ongaku --depth=1 && cd ongaku && pip install virtualenv && virtualenv venv && source venv/bin/activate
```

```
pip install -r requirements.txt && exit && cd .. && termux-notification-list
```

You will be asked to provide notification access to Termux:API app. You must provide Termux:API app all the required permissions. You may be required to do `Ctrl+C` to continue.

* When you run the Ongaku for the first time you are asked to enter your phone number to create a session. Ongaku uses this session to work with your telegram account.

* Create a `config.env` file from `sample-config.env`

$ `cd ongaku && cp sample-config.env config.env`

Edit `config.env` as instructed by the file itself.

$ `nano config.env`

Use `Ctrl+X` to save your changes.

* Start playing music using the app you set in `config.env` and `./launch.sh` inside `ongaku` directory.

* If this is your first time launching Ongaku then you will be asked to enter your phone number to login. Next launches will work without having to re-login.

* If everything went well you should get `Ongaku started` in your saved messages. And you should see current playing song in the Termux app and in the telegram channel you set for logging if any.

* From notifications tap on `ACQUIRE WAKELOCK` on termux notification and allow access to let Termux run in background. This needs to be done each time you  relaunch termux.

### Known Limitations

* Ongaku cannot yet differentiate between the states of music player itself i.e. `Playing`, `Paused` and `Stopped`. It simply assumes existing music player notification as a `Playing` state.
* It is not yet possible to run Ongaku on a baremetal server or a VPS/PaaS such as Heroku.
* Devices running MIUI are unsupported as Xiaomi loves to revoke notification permission after X amount of hours and even at each device reboot. However you can still use Ongaku if you are willing to provide notification access manually from `Settings` app each time Ongaku starts malfunctioning! This is something you can also fix by running a reputable custom rom such as [LineageOS](https://lineageos.org/). (**#RipBozo** 💯🤣🤣 if you choose to run MIUI on your phone anyway)

### Optional commands
Send in any telegram chat

`.about` to view info about the project.

`.history` to get list of music played in current session.

`.sync` to force sync bio with latest notification.

### Authors
* [Shouko](https://github.com/gibcheesepuffs)
* [Ryuk](https://github.com/anonymousx97)

### Support
[Shouko's Lab](https://t.me/shoukolab)

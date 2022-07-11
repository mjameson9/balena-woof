# balena-woof
Turn a Raspberry Pi into a button your dog or cat can use to convey a message to you. Handy for dogs that need a better way to get your attention when they want to eat or go outside.

![assembled](https://user-images.githubusercontent.com/101855796/178084462-61c4643f-2195-4a17-9451-060e2ce3e6b7.jpeg)


## Overview
Here are the features of balena-woof

Produces a sound and notification when button is pressed
Sound can be adjusted using an environmental variable. Several sounds are included, but more can be added easily
Has an adjustable "cooldown" to prevent spamming
Utilizes an LED to show when the cooldown has ended
Sends anvia SendGrid email if addresses and API are configured

## Building the device

The device consists of the following components:
- Raspberry Pi
- Button
- Speaker
- Wire

![assembly diagram](https://user-images.githubusercontent.com/101855796/178084327-a7116ce6-2235-444b-82f0-1a0a83b901d8.jpg)

In its most basic form, the device is simply a speaker, a button and an LED plugged into a Raspberry Pi. My main draft of the device included a breadboard and 4 additional green LEDs to signify different things, but in the end I diverted my focus back to other features that were not dependant on the additional hardware. So if you want to build this, you should be able to plug in a usb speaker and wire the button and LED and call it done! Hopefully I'll be able to add some additional features that will make use of additional add-ons later down the line.

## How it works

We use the balena platform to run two containers on the device. Each container provides separate functionality.

### Audio
This is our beloved audio block that runs a PulseAudio server optimized for balenaOS and is the core of balenaSound. We use it here to take care of setting up and routing all audio needs on the Pi hardware, so the noise container just sends its audio here.

### Woofer
A custom python program that interprets GPIO input and plays the wav file using the audio block.

## Setting it up

Assuming you have it built out and put in an enclosure of your choosing, all that's left is some slight configuration. Out of the box the device is configured to play the 'default' sound. If you were to hit that button immediately after deploying the application, the voice will tell you you need to map a sound using the environmental variable. To adjust this, simply modify the variable to one of the following included sound files:
- outside.wav
- hungry.wav
- sorry dave.wav

You can also easily include your own sounds! Just make sure you convert them to a 16-bit PCM WAV file so they are compatible with pygame. Audacity is a good tool for this.

**Quick note**: *If that voice sounds familiar, you must be a gamer! I made those voice lines using a text to speech application based on GLADOS from the Portal series. The tool I used can be found here:*
https://glados.c-net.org

By default, the button has a 5 second cooldown. This is to prevent your puppy from spamming the button. If you wish to shorten or extend this, simply modify the 'TIMEOUT_LIMIT' environmental variable.

Finally, there is also a feature to send you an email when the button is pressed. This is handy if you want to know your dog pressed the button when you weren't around. This involves setting up a SendGrid account and verified sender. Their free plan lets you send 100 emails a day, which should hopefully be sufficient for this purpose. I won't go into how to set that up since their documentation covers it pretty well, just know that you need to put your 'to' and 'from' addresses into woofer.py, as well as include your API key using the 'SENDGRID_API_KEY' environmental variable.

## Environmental variables

The following environment variables allow some degree of configuration:

| Environment variable | Description | Default | Options | 
| --- | --- | --- | --- |
| `AUDIO_OUTPUT` | Select the default audio output device. <br>Can also be changed at runtime by using the [companion library](#companion-library) | `AUTO` | For all device types: <br>- `AUTO`: Let PulseAudio decide. Priority is `USB > DAC > HEADPHONES > HDMI`<br>- `DAC`: Force default output to be an attached GPIO based DAC<br>- `<PULSE_SINK_NAME>`: If you know the sink name you can force set it too. Note that you can't use this to set custom sinks as default, in that case use `set-default-sink` on your custom pa script. <br><br> For Raspberry Pi devices: <br>- `RPI_AUTO`: BCM2835 automatic audio switching as described [here](https://web.archive.org/web/20200427023741/https://www.raspberrypi.org/documentation/configuration/audio-config.md). Deprecated for devices running Linux kernel 5.4 or newer. <br>- `RPI_HEADPHONES`: 3.5mm audio jack <br>- `RPI_HDMI0`: Main HDMI port <br>- `RPI_HDMI1`: Secondary HDMI port (only Raspberry Pi 4) <br><br> For Intel NUC: <br>- NUCs have automatic output detection and switching. If you plug both the HDMI and the 3.5mm audio jack it will use the latter.  |
| `AUDIO_VOLUME` | Initial volume level for the default audio output device. | `75%` | Any value between 0-100%. |
| `SENDGRID_API_KEY` | Your unique generated API from SendGrid to allow email notifications. |  | Specific case sensitive key. |
| `SOUND_FILE` | Sound file you want the device to play. More can be added by dropping audio files in the 'woofer' folder. | `default.wav` | -`default.wav`: "Please select an environmental variable" <br><br>- `outside.wav`: "Outside" <br><br>- `hungry.wav`: "I'm hungry" <br><br>- `sorry dave.wav`: "I'm sorry Dave, I'm afraid I can't do that. <br>
| `TIMEOUT_LIMIT` | The ammount of seconds the device spends in 'cooldown' after a successful push. | `5` | Any interger |

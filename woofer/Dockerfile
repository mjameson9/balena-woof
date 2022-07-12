FROM balenalib/raspberrypi3-python:3.7-build-20210705

WORKDIR /usr/src/app

RUN \
    apt-get update && apt-get install -y python3-pygame libfreetype6-dev # Needed for Pillow font use

RUN \
    pip3 install requests RPi.GPIO sendgrid

COPY *.py ./
COPY *.wav ./

CMD [ "python3", "woofer.py" ]

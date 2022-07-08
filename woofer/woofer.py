import pygame
import RPi.GPIO as GPIO 
import time
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email():
    if sendgrid_api_key != '':
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        from_email = Email("matthew.jameson@balena.io")  # Change to your verified sender
        to_email = To("mattjamesonit@gmail.com")  # Change to your recipient
        subject = "Woofer button pressed!"
        content = Content("text/plain", "Hello, this e-mail was triggered by button press number {}!".format(count))
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        print("Email sent, response status: {}".format(response.status_code))
        print("Email response headers: {}". format(response.headers))

# Initialize global variables
count = 0  # count of button presses
timeout = 0  # count of seconds after button press

# Get device variables
try:
    timeout_limit = int(os.getenv('TIMEOUT_LIMIT', '5'))
except Exception as e:
    print("Invalid value for TIMEOUT_LIMIT. Using default 5.")
    timeout_limit = 5

sendgrid_api_key = os.getenv('SENDGRID_API_KEY', '')
if sendgrid_api_key == '':
    print("Warning, SENDGRID_API_KEY is not set! You can't send e-mails!")

# Setup for sounds
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.mixer.init()

# Initialize pygame
#pygame.init()
  
# Load all sound files
outside_sound = pygame.mixer.Sound("outside.wav")

# Set GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

# Function below only called when button is pressed:
def button_press(channel):

    global count, timeout

    count = count + 1
    print("timeout: {}".format(timeout))
    if timeout == 0:
        # No timeout is set; start the timeout
        timeout = 1
        outside_sound.play()
        send_email()
        GPIO.output(20, GPIO.LOW)
        print("Button press number {}!".format(count))
    else:
        if timeout >= (timeout_limit + 1):
            timeout = 1
            outside_sound.play()
            send_email()
            GPIO.output(20, GPIO.LOW)
            print("Button press number {}!".format(count))

# Set GPIO button input
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(21, GPIO.RISING, callback=button_press, bouncetime=500)

# Setup GPIO LED outputs
GPIO.setup(5, GPIO.OUT) # Green LED 1
GPIO.setup(6, GPIO.OUT) # Green LED 2
GPIO.setup(13, GPIO.OUT) # Green LED 3
GPIO.setup(19, GPIO.OUT) # Green LED 4
GPIO.setup(20, GPIO.OUT) # Red button LED

# Set all LEDs off initially
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW)
GPIO.output(20, GPIO.HIGH)


# Loop forever until CTRL+C pressed:

while True:

    time.sleep(1)
    
    if timeout > 0:
        timeout = timeout + 1
        if timeout >= (timeout_limit + 1):
            timeout = 0
            GPIO.output(20, GPIO.HIGH)

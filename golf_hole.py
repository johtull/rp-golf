import RPi.GPIO as GPIO
import time
import requests

# Ground on 30
HoleLedPin = 29
ToggleLedPin = 32
# 3V Power on 1 to Red
# Blue to 36
HoleBtnPin = 31   # button pressed when you score
ToggleBtnPin = 33 # toggle test_mode

test_mode = True # test_mode will not invoke the
last_call = time.time() - 5

OnUrl = ""
OffUrl = ""

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(HoleLedPin, GPIO.OUT) # Hole LED
GPIO.setup(ToggleLedPin, GPIO.OUT) # Toggle LED
GPIO.setup(HoleBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Hole Button
GPIO.setup(ToggleBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Toggle Button
GPIO.output(ToggleLedPin, GPIO.HIGH)

def req(on):
    if on:
        URL = OnUrl
    else:
        URL = OffUrl
    
    r = requests.get(url = URL)
    #print(str(r.status_code))
    
    # test POST
    #location = "Chicago, IL"
    #PARAMS = {'address':location}
    #r = requests.get(url = URL, params = PARAMS)
    #data = r.json()
    #latitude = data['results'][0]['geometry']['location']['lat']
    #longitude = data['results'][0]['geometry']['location']['lng']
    #formatted_address = data['results'][0]['formatted_address']
    #print(str(latitude) + ", " + str(longitude))
	

# if the user scores, light the LED
# if not in test mode, POST to turn on light
def score(channel):
    global last_call
    global test_mode
    #print("last_call: " + str(last_call))
    #print("test_mode: " + str(test_mode))
    #print("time(): " + str(time.time()))
    
    # if last execution was more than 5 seconds ago, score
    # this prevents duplicate callbacks
    # TODO: MAKE THIS BETTER
    if time.time() > last_call + 5:
        GPIO.output(HoleLedPin, GPIO.HIGH)
        # if not in test mode, POST
        if not test_mode:
            req(False)
            time.sleep(3)
            req(True)
        else:
            time.sleep(3)
        
        # turn off hole led
        GPIO.output(HoleLedPin, GPIO.LOW)
        
        # set the last call time
        last_call = time.time()
        
def toggle(channel):
    global test_mode
    test_mode = not test_mode
    if test_mode:
        GPIO.output(ToggleLedPin, GPIO.HIGH)
    else:
        GPIO.output(ToggleLedPin, GPIO.LOW)

GPIO.add_event_detect(HoleBtnPin, GPIO.RISING, callback=score, bouncetime=1000)
GPIO.add_event_detect(ToggleBtnPin, GPIO.RISING, callback=toggle, bouncetime=1000)

try:
    while True:
        i = 0
except KeyboardInterrupt:
    print("Keyboard interrupt")
finally:
    GPIO.cleanup()

# rp-golf
Logic for the automated golf hole.  

This script was designed for a Raspberry Pi 3 to control 2 buttons and 2 LEDs, all connected to a breadboard.  

The "Hole Button" triggers when someone has scored. It turns on the Hole LED and conditionally triggers a GET request.   
The "Toggle Button" toggles test_mode.  While test_mode is True, the Toggle LED will be on.  

When test_mode is activated, the Hole Button simply turns on the Hole LED. When it is not active, the Hole Button will trigger a GET request to activate a light connect to a WeMo and controlled by an AWS service.  

Pins:  
HoleLedPin = 29  
Ground = 30  
HoleBtnPin = 31  
ToggleLedPin = 32  
ToggleBtnPin = 33  
  

import json
from vulcan import Vulcan
       
        
DOMAIN = "vulcan"

def setup(hass, config):
    hass.states.set("vulcan.test", "Sing in successfully")

    # Return boolean to indicate that initialization was successful.
    return True



import json
from vulcan import Vulcan
def reg(token, symbol, pin):
    certificate = Vulcan.register(token, symbol, pin)
    with open('cert.json', 'w') as f: 
        json.dump(certificate.json, f)
        
DOMAIN = "vulcan"

def setup(hass, config):
    hass.states.set("vulcan.world", "Sing in successfully")

    # Return boolean to indicate that initialization was successful.
    return True


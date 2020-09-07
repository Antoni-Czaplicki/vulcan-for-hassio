DOMAIN = "vulcan"


def setup(hass, config):
    hass.states.set("vulcan.world", "Sing in successfully")

    # Return boolean to indicate that initialization was successful.
    return True

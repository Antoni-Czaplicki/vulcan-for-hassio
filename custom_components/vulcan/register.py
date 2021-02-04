import json
from pathlib import Path

from vulcan import Account, Keystore, Vulcan, VulcanHebe

from . import DOMAIN


def reg(token, symbol, pin):
    certificate = Vulcan.register(token, symbol, pin, "Home Assistant")
    with open("vulcan.json", "w") as f:
        json.dump(certificate.json, f)

    return None


async def register(token, symbol, pin):
    Path(".vulcan").mkdir(parents=True, exist_ok=True)
    keystore = Keystore.create(device_model="Home Assistant")
    account = await Account.register(keystore, token, symbol, pin)
    with open(".vulcan/keystore-" + account.user_login + ".json", "w") as f:
        f.write(keystore.as_json)
    with open(".vulcan/account-" + account.user_login + ".json", "w") as f:
        f.write(account.as_json)
    return {"account": account, "keystore": keystore}

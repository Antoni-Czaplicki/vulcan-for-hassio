import json
from pathlib import Path

from vulcan import Account, Keystore 

from . import DOMAIN


async def register(token, symbol, pin):
    Path(".vulcan").mkdir(parents=True, exist_ok=True)
    keystore = Keystore.create(device_model="Home Assistant")
    account = await Account.register(keystore, token, symbol, pin)
    with open(f".vulcan/keystore-{account.user_login}.json", "w") as f:
        f.write(keystore.as_json)
    with open(f".vulcan/account-{account.user_login}.json", "w") as f:
        f.write(account.as_json)
    return {"account": account, "keystore": keystore}

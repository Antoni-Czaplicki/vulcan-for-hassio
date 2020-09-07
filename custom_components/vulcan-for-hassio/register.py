def register(token, symbol, pin)
    certificate = Vulcan.register(token, symbol, pin)
    with open('cert.json', 'w') as f: 
        json.dump(certificate.json, f)


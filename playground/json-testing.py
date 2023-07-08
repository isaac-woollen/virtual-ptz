import json

def set_client_config(ip, port):
    config_init = {
        "vptz-ip" : ip,
        "vptz-port": port
    }

    config = json.dumps(config_init, indent=4)

    with open("client/server/config.json", "w") as outfile:
        outfile.write(config)
        outfile.close()

set_client_config("192.168.1.1", "8777")
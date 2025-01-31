import requests

# ipify API will return the public IP address of the requestor
def get_ip():
    res = requests.get("https://api.ipify.org")
    return (res.status_code, res.text)
import random
from config import PROXIES_FILE

def load_proxies():
    with open(PROXIES_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def get_random_proxy():
    proxies = load_proxies()
    return random.choice(proxies)

def parse_proxy(proxy_line):
    if "@" in proxy_line:
        # صيغة Bright Data
        auth, host = proxy_line.strip().split("@")
        username, password = auth.split(":")
        ip, port = host.split(":")
    else:
        # الصيغة التقليدية: IP:PORT:USERNAME:PASSWORD
        ip, port, username, password = proxy_line.strip().split(":")

    return {
        "server": f"http://{ip}:{port}",
        "username": username,
        "password": password
    }


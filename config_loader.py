import json
import os

def load_site_config(site_name):
    path = os.path.join("sites", f"{site_name}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


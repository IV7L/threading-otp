import os
import json
# config.py
from config_loader import load_site_config

GROUP_PATH = "group1"
NUMBERS_FILE = os.path.join(GROUP_PATH, "access_numbers.txt")
PROXIES_FILE = os.path.join(GROUP_PATH, "proxies.txt")
CAPTCHA_KEYS_FILE = os.path.join(GROUP_PATH, "captcha_keys.txt")

# الموقع الافتراضي (يمكنك تغييره من السطر التالي)
SELECTED_SITE = "w1"

# تحميل الإعدادات من ملف JSON في مجلد sites/
SITE_CONFIG = load_site_config(SELECTED_SITE)

MAX_WORKERS = 25

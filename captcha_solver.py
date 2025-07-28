import requests
import time
import random
from config import CAPTCHA_KEYS_FILE
from config_loader import load_site_config as config  # ✅ استيراد إعدادات الموقع

def load_captcha_keys():
    with open(CAPTCHA_KEYS_FILE, "r") as f:
        return [key.strip() for key in f.readlines() if key.strip()]

captcha_keys = load_captcha_keys()

def get_captcha_token(config):
    api_key = random.choice(captcha_keys)
    print(f"[🔐] استخدام مفتاح 2Captcha: {api_key[:6]}...")

    url = "http://2captcha.com/in.php"

    method = "userrecaptcha" if config.get("captcha_type", "recaptcha") == "recaptcha" else "hcaptcha"

    captcha_payload = {
        "key": api_key,
        "method": method,
        "googlekey": config["site_key"],
        "pageurl": config["site_url"],
        "json": 1
    }

    r = requests.post(url, data=captcha_payload)
    res = r.json()
    if res["status"] != 1:
        raise Exception(f"خطأ في إرسال التحدي إلى 2Captcha: {res}")

    rid = res["request"]
    fetch_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={rid}&json=1"

    for i in range(30):
        print(f"[⌛️] محاولة {i+1}/30 للحصول على التوكن...")
        time.sleep(5)
        res = requests.get(fetch_url).json()
        if res["status"] == 1:
            print(f"[🔓] ✅ توكن جاهز!")
            return res["request"]

    raise Exception("⏱ انتهاء وقت الانتظار للحصول على التوكن")

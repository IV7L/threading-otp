import json
from playwright.async_api import async_playwright
from config import SITE_CONFIG
from captcha_solver import get_captcha_token
from utils import get_random_proxy, parse_proxy
from logger import log

async def handle_number(phone, browser):
    try:
        # تحميل بروكسي عشوائي وإنشاء السياق
        proxy_line = get_random_proxy()
        proxy = parse_proxy(proxy_line)

        context = await browser.new_context(proxy=proxy)
        page = await context.new_page()

        # الانتقال إلى صفحة التسجيل
        await page.goto(SITE_CONFIG["site_url"], wait_until="domcontentloaded")
        print(f"[{phone}] ✅ فتح الصفحة: {SITE_CONFIG['site_url']}")

        # إدخال الرقم في الحقل
        await page.locator(SITE_CONFIG["phone_input_xpath"]).fill(phone)
        print(f"[{phone}] 📝 أدخل الرقم في الحقل")

        # حل الكابتشا
        token = get_captcha_token(SITE_CONFIG)
        print(f"[{phone}] 🔓 تم حل الكابتشا: {token[:20]}...")

        # تجهيز الطلب لإرساله
        api_conf = SITE_CONFIG["fetch_api_request"]
        headers = api_conf["headers"]
        body_dict = api_conf["body"].copy()

        # استبدال رقم الهاتف
        body_dict["login"] = phone

        # استبدال توكن الكابتشا
        for key, val in body_dict.items():
            if isinstance(val, str) and val == "INJECT_DYNAMIC_SIGNATURE":
                body_dict[key] = token

        # تحويل الجسم إلى JSON
        body_json = json.dumps(body_dict)

        # بناء كود جافاسكريبت للتنفيذ داخل الصفحة
        fetch_code = f"""
        fetch("{api_conf['url']}", {{
          method: "{api_conf['method']}",
          headers: {json.dumps(headers)},
          body: JSON.stringify({body_json})
        }})
        .then(res => res.json())
        .then(data => console.log("✅ Server Response:", data))
        .catch(err => console.error("❌ Error in request:", err));
        """
        await page.evaluate(fetch_code)
        print(f"[{phone}] 🚀 تم إرسال الطلب من داخل المتصفح")

        # تسجيل النجاح
        log("success.log", f"{phone} ✅ تم الإرسال")
        await page.close()
        await context.close()

    except Exception as e:
        log("error.log", f"{phone} ❌ فشل → {e}")
        print(f"[{phone}] ❌ خطأ: {e}")

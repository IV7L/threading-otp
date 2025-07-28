import asyncio
from config import NUMBERS_FILE, MAX_WORKERS
from worker import handle_number
from logger import log
from playwright.async_api import async_playwright
from config_loader import load_site_config

# 🟡 ضع اسم الموقع هنا أو اجعلها ديناميكية من سطر الأوامر
site_name = "w1"
SITE_CONFIG = load_site_config(site_name)

with open(NUMBERS_FILE, "r") as f:
    numbers = [line.strip() for line in f.readlines() if line.strip()]

async def main():
    sem = asyncio.Semaphore(MAX_WORKERS)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        async def sem_task(phone):
            async with sem:
                await handle_number(phone, browser)

        tasks = [sem_task(num) for num in numbers]
        await asyncio.gather(*tasks)
        log("general.log", f"تم تنفيذ {len(tasks)} رقم.")

if __name__ == "__main__":
    asyncio.run(main())

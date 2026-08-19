from playwright.sync_api import sync_playwright
from scraper import get_match_details

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://www.basquetcatala.cat/equip/89676"
    )

    page.wait_for_timeout(5000)

    info = get_match_details(
        page,
        "11984"
    )

    print(info)

    browser.close()
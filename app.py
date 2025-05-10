import asyncio
from playwright.async_api import async_playwright, Playwright
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import ast
import pandas as pd
from datetime import datetime, timedelta
import re
import numpy as np
from logger_creator import logger_all

# Function to scrape data
async def scrape_data(playwright: Playwright, url: str):
    args = ["--disable-blink-features=AutomationControlled"]
    browser = await playwright.chromium.launch(headless=False, args=args)
    page = await browser.new_page()
    logger_all.info(f'Loading Web page {url}...')
    await page.goto(url)

    # Handle cookie consent prompt
    try:
        # Wait for the cookie consent button to appear and click it
        await page.wait_for_selector('#didomi-notice-agree-button', timeout=5000)  # Wait up to 5 seconds
        cookie_button = await page.query_selector('#didomi-notice-agree-button')
        if cookie_button:
            await cookie_button.click()
            logger_all.info(f'Cookie consent dismissed.')
            time.sleep(1)  # Brief pause to ensure action is processed
    except Exception as e:
        logger_all.info(f'No cookie consent prompt found or clickable')

    main_content = await page.content()
    data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
    }

    #load data into a DataFrame object:
    df = pd.DataFrame(data)
    df.to_excel('data.xlsx', index=False)
    await browser.close()

# Main function to run the scraper
async def main(url: str):
    async with async_playwright() as playwright:
        await scrape_data(playwright, url)


# Entry point of the script
if __name__ == "__main__":
    start = time.time()
    url: str = 'https://www.fotocasa.es/es/alquiler/viviendas/barcelona-provincia/baix-llobregat/l'  # "https://www.fotocasa.es/es/comprar/viviendas/barcelona-provincia/garraf/l"
    asyncio.run(main(url))
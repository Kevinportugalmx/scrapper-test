import time
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_driver() -> webdriver.Firefox:
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Firefox(options=firefox_options)


def extract_product_data(section) -> dict:
    name = section.select_one("span.vtex-product-summary-2-x-productBrand")
    price = section.select_one("div.tiendasjumboqaio-jumbo-minicart-2-x-price")
    promo_price = section.select_one(
        "div.tiendasjumboqaio-jumbo-minicart-2-x-cencoListPriceWrapper"
    )

    return {
        "name": name.get_text(strip=True) if name else None,
        "price": (
            promo_price.get_text(strip=True)
            if promo_price
            else price.get_text(strip=True) if price else None
        ),
        "promo_price": price.get_text(strip=True) if promo_price else None,
    }


def jumbo_service(url: str):
    print("\n" + url + "\n")

    start_time = time.time()
    driver = create_driver()
    logger.info(f"Driver created in {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    driver.get(url)
    logger.info(f"Page loaded in {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    products = []
    scroll_pause_time = 1.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    while len(products) < 15:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_sections = soup.select(
            "section.vtex-product-summary-2-x-container.vtex-product-summary-2-x-containerNormal"
        )
        products.extend(
            extract_product_data(section)
            for section in product_sections
            if len(products) < 15
        )
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    logger.info(f"Scraped in {time.time() - start_time:.2f} seconds")
    logger.info(f"Scraped {len(products)} products")

    driver.quit()
    return products

import time
import logging
from playwright.sync_api import sync_playwright
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_product_data(section) -> dict:
    name = section.query_selector("span.vtex-product-summary-2-x-productBrand")
    price = section.query_selector("div.tiendasjumboqaio-jumbo-minicart-2-x-price")
    promo_price = section.query_selector(
        "div.tiendasjumboqaio-jumbo-minicart-2-x-cencoListPriceWrapper"
    )

    return {
        "name": name.inner_text().strip() if name else None,
        "price": (
            promo_price.inner_text().strip()
            if promo_price
            else price.inner_text().strip() if price else None
        ),
        "promo_price": price.inner_text().strip() if promo_price else None,
    }


def jumbo_service(url: str):
    init_service = time.time()
    print("\n" + url + "\n")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 1080},
        )

        context.route(
            "**/*",
            lambda route, request: (
                route.abort()
                if request.resource_type in ["image", "stylesheet", "font"]
                else route.continue_()
            ),
        )

        page = context.new_page()

        start_time = time.time()
        page.goto(url, wait_until="domcontentloaded")
        logger.info(f"Page loaded in {time.time() - start_time:.2f} seconds")

        try:
            page.wait_for_selector(
                "section.vtex-product-summary-2-x-container.vtex-product-summary-2-x-containerNormal",
                timeout=10000,
            )
        except Exception as e:
            logger.error(
                "Error: El div específico no se encontró en la página. Detalle: %s",
                str(e),
            )
            browser.close()
            raise HTTPException(
                status_code=408, detail="Timeout Error: Webpage not found"
            )

        total_products_found = 0
        max_products = 15
        products = []

        while total_products_found < max_products:
            product_sections = page.query_selector_all(
                "section.vtex-product-summary-2-x-container.vtex-product-summary-2-x-containerNormal"
            )

            for section in product_sections:
                if total_products_found < max_products:
                    product_data = extract_product_data(section)
                    if product_data["name"]:
                        products.append(product_data)
                        total_products_found += 1
                        logger.info(f"Product found: {product_data['name']}")

            page.evaluate("window.scrollBy(0, window.innerHeight);")
            time.sleep(0.5)

            if len(products) >= max_products:
                logger.info(f"Found {len(products)} products, starting extraction.")
                break

        logger.info(
            f"Extracted data for {len(products)} products in {time.time() - start_time:.2f} seconds"
        )
        browser.close()
        logger.info(f"Total time: {time.time() - init_service:.2f} seconds")
        return products[:max_products]

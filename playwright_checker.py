from playwright.sync_api import sync_playwright
import time
import logging
import random
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_checker.log'),
        logging.StreamHandler()
    ]
)

class JellycatStockChecker:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            args=['--window-size=1920,1080']
        )
        
    def check_product_availability(self, url: str, product_name: str) -> Optional[bool]:
        """
        Check if a product is in stock using Playwright
        Returns:
            - True if in stock
            - False if out of stock
            - None if error occurred
        """
        try:
            page = self.browser.new_page()
            
            # Add debug logging
            logging.debug(f"Navigating to {url}")
            page.goto(url)
            
            # Increase timeout during testing
            logging.debug("Waiting for add to cart button...")
            try:
                add_to_cart_button = page.wait_for_selector(
                    'input.button.button--primary.tw-w-full.tw-whitespace-normal[type="submit"]',
                    timeout=10000
                )
            except TimeoutError:
                # Take screenshot when element not found
                page.screenshot(path=f"debug_{product_name}_timeout.png")
                raise
            
            # Add more detailed logging
            button_value = add_to_cart_button.get_attribute('value').lower()
            logging.debug(f"Button value: {button_value}")
            
            is_in_stock = 'out of stock' not in button_value
            
            status = "IN STOCK" if is_in_stock else "OUT OF STOCK"
            logging.info(f"{product_name}: {status}")
            
            page.close()
            return is_in_stock
            
        except Exception as e:
            # Take screenshot on any error
            try:
                page.screenshot(path=f"debug_{product_name}_error.png")
            except:
                pass
            raise

    def monitor_product(self, url: str, product_name: str, check_interval: int = 300):
        """
        Continuously monitor a product's availability
        Args:
            url: Product URL
            product_name: Name of the product
            check_interval: Time between checks in seconds (default 5 minutes)
        """
        previous_status = None
        
        try:
            while True:
                try:
                    jitter = random.uniform(-30, 30)  # ±30 seconds
                    actual_interval = check_interval + jitter
                    
                    current_status = self.check_product_availability(url, product_name)
                    
                    if current_status is not None and current_status != previous_status:
                        if previous_status is not None:
                            status_str = "IN STOCK" if current_status else "OUT OF STOCK"
                            message = f"Status change for {product_name}: {status_str}"
                            logging.info(message)
                        
                        previous_status = current_status
                    
                    time.sleep(actual_interval)
                    
                except Exception as e:
                    logging.error(f"Unexpected error monitoring {product_name}: {str(e)}")
                    time.sleep(min(actual_interval * 2, 3600))  # Max 1 hour
                    
        finally:
            self.browser.close()
            self.playwright.stop()

def main():
    checker = JellycatStockChecker()
    
    # Test cases
    test_products = [
        {
            "url": "https://us.jellycat.com/bashful-grey-kitty/",
            "name": "Bashful Grey Kitty"
        },
        # Add more test products here
        {
            "url": "https://us.jellycat.com/bashful-winter-puppy/",
            "name": "Bashful Winter Puppy"
        }
    ]
    
    # Test single check
    for product in test_products:
        result = checker.check_product_availability(product["url"], product["name"])
        print(f"Test result for {product['name']}: {result}")
    
    # Uncomment to test monitoring
    # checker.monitor_product(test_products[0]["url"], test_products[0]["name"], check_interval=60)  # Shorter interval for testing

if __name__ == "__main__":
    # Set logging to DEBUG level during testing
    logging.getLogger().setLevel(logging.DEBUG)
    main()

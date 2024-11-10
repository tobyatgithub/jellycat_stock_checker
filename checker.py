from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import random
from typing import Optional

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# driver = webdriver.Chrome(
# 	service=Service(ChromeDriverManager().install()),
# 	options=chrome_options
# )

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
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Run in headless mode
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920,1080')
        
        # Add random user agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        self.options.add_argument(f'user-agent={user_agent}')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )
        self.wait = WebDriverWait(self.driver, 10)
        
    def check_product_availability(self, url: str, product_name: str) -> Optional[bool]:
        """
        Check if a product is in stock using Selenium
        Returns:
            - True if in stock
            - False if out of stock
            - None if error occurred
        """
        try:
            self.driver.get(url)
            
            # Wait for the add to cart button to be present
            add_to_cart_button = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'input.button.button--primary.tw-w-full.tw-whitespace-normal[type="submit"]'
                ))
            )
            
            button_value = add_to_cart_button.get_attribute('value').lower()
            is_in_stock = 'out of stock' not in button_value
            
            status = "IN STOCK" if is_in_stock else "OUT OF STOCK"
            logging.info(f"{product_name}: {status}")
            
            return is_in_stock
            
        except TimeoutException:
            logging.error(f"Timeout waiting for elements on {product_name}")
            return None
        except Exception as e:
            logging.error(f"Error checking {product_name}: {str(e)}")
            return None

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
            self.driver.quit()

def main():
    checker = JellycatStockChecker()
    
    # Example usage
    product_url = "https://us.jellycat.com/bashful-grey-kitty/"
    # product_url = "https://us.jellycat.com/jollipop-cat/"
    # product_name = "Jollipop Cat"
    product_name = "cat Cat"
    
    # Monitor with 5-minute intervals
    checker.monitor_product(product_url, product_name, check_interval=300)

if __name__ == "__main__":
    main()
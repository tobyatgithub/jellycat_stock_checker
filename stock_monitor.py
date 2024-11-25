import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from playwright_checker import JellycatStockChecker
from wechat_notification import WeChatNotifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("stock_monitor.log"), logging.StreamHandler()],
)


@dataclass
class Product:
    url: str
    name: str
    previous_status: bool = None


class StockMonitor:
    def __init__(self):
        self.checker = JellycatStockChecker()
        self.notifier = WeChatNotifier()

    def format_stock_message(self, products_status: List[Dict]) -> str:
        """Format the stock status message for WeChat notification"""
        # Get current time in desired format
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M")

        message_parts = [
            "🧸 Jellycat Stock Update 🧸",
            f"📅 {current_time}\n",  # Add timestamp
        ]

        for product in products_status:
            status = "✅ IN STOCK" if product["in_stock"] else "❌ OUT OF STOCK"
            message_parts.append(f"{product['name']}: {status}")
            message_parts.append(f"URL: {product['url']}\n")

        return "\n".join(message_parts)

    def check_and_notify(self, products: List[Product]):
        """Check stock status and send notifications for changes"""
        try:
            products_with_changes = []

            for product in products:
                current_status = self.checker.check_product_availability(
                    product.url, product.name
                )

                # If this is the first check or status has changed
                if (
                    product.previous_status is None
                    or product.previous_status != current_status
                ):
                    products_with_changes.append(
                        {
                            "name": product.name,
                            "url": product.url,
                            "in_stock": current_status,
                        }
                    )

                    product.previous_status = current_status

            # If there are any changes, send notification
            if products_with_changes:
                message = self.format_stock_message(products_with_changes)
                success = self.notifier.send_message(message)

                if success:
                    logging.info("Notification sent successfully")
                else:
                    logging.error("Failed to send notification")

        except Exception as e:
            error_message = f"Error during stock check: {str(e)}"
            logging.error(error_message)
            self.notifier.send_message(f"⚠️ Monitor Error ⚠️\n{error_message}")


def main():
    # Define products to monitor
    products = [
        Product(
            url="https://us.jellycat.com/bashful-grey-kitty/", name="Bashful Grey Kitty"
        ),
        Product(
            url="https://us.jellycat.com/bashful-winter-puppy/",
            name="Bashful Winter Puppy",
        ),
        # Add more products as needed
    ]

    monitor = StockMonitor()

    # Single check for testing
    monitor.check_and_notify(products)

    # For continuous monitoring, you could add:
    # while True:
    #     monitor.check_and_notify(products)
    #     time.sleep(300)  # Check every 5 minutes


if __name__ == "__main__":
    main()

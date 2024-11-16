# Jellycat Stock Checker

A simple tool to monitor stock availability of Jellycat products using web automation. The project includes two implementations:

- `checker.py`: Uses Selenium WebDriver
- `playwright_checker.py`: Uses Playwright

## Features
- Continuous monitoring of product availability
- Random intervals between checks to avoid detection
- Detailed logging of stock changes
- Debug screenshots on errors (Playwright version)

## Requirements
- Python 3.10+
- Chrome browser
- Required packages:
  - Selenium implementation: `selenium`, `webdriver_manager`
  - Playwright implementation: `playwright`

## Installation
```bash
#Install dependencies for Selenium version
pip install selenium webdriver_manager

# OR for Playwright version
pip install playwright
playwright install chromium
```

## Usage
```python
# Using Selenium version
from checker import JellycatStockChecker

# OR using Playwright version
from playwright_checker import JellycatStockChecker
# Monitor a product
checker = JellycatStockChecker()
checker.monitor_product(
url="https://us.jellycat.com/bashful-grey-kitty/",
product_name="Bashful Grey Kitty",
check_interval=300 # 5 minutes
)
```

The script will continuously monitor the product and log any stock changes to both console and `stock_checker.log`.
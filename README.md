# Jellycat Stock Checker

A simple tool to monitor stock availability of Jellycat products using web automation. The project includes two implementations:

- `checker.py`: Uses Selenium WebDriver
- `playwright_checker.py`: Uses Playwright

## Features
- Continuous monitoring of product availability
- Random intervals between checks to avoid detection
- Detailed logging of stock changes
- Debug screenshots on errors (Playwright version)
- WeChat notifications support 

## Requirements
- Python 3.10+
- Chrome browser
- Required packages:
  - Selenium implementation: `selenium`, `webdriver_manager`
  - Playwright implementation: `playwright`
  - WeChat notifications: TBD (under development)

## Installation
```bash
# Install dependencies for Selenium version
pip install selenium webdriver_manager

# OR for Playwright version
pip install playwright
playwright install chromium

# WeChat notification support will be added soon
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
    check_interval=300  # 5 minutes
)
```

The script will continuously monitor the product and log any stock changes to both console and `stock_checker.log`.

## WeChat Notifications
通过企业微信的微信插件功能实现推送到个人微信。此功能参考了 [wecomchan](https://github.com/easychen/wecomchan) 项目的实现方案。

### 配置步骤:

1. 注册企业微信并创建应用
2. 在应用管理中获取:
   - 企业ID (corpid)
   - 应用ID (agentid) 
   - 应用Secret (secret)
3. 在"我的企业" → "微信插件"中:
   - 扫码关注以接收消息
   - 勾选"允许成员在微信插件中接收和回复聊天消息"
4. 在企业微信客户端的设置中关闭"仅在企业微信中接受消息"限制

### 限制说明:
- 接收消息的用户需要是该企业微信下的成员
- 每个企业微信可以免费添加200个成员
- 消息推送无需认证即可使用

### 优点:
- 配置简单,无需额外服务
- 消息可直接推送到个人微信
- 无需安装企业微信客户端
- 免费使用


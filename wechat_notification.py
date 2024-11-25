import json
import logging
import os
from typing import Optional

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("wechat_notification.log"), logging.StreamHandler()],
)


class WeChatNotifier:
    def __init__(self):
        # Corporate WeChat configurations
        self.corpid = os.getenv("CORP_ID")  # 企业ID
        self.corpsecret = os.getenv("CORP_SECRET")
        self.agentid = os.getenv("AGENT_ID")  # 应用ID
        self.token = None

    def get_access_token(self) -> Optional[str]:
        """Get access token from WeChat API"""
        try:
            url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
            response = requests.get(url)
            data = response.json()

            if data["errcode"] == 0:
                return data["access_token"]
            else:
                logging.error(f"Failed to get access token: {data}")
                return None

        except Exception as e:
            logging.error(f"Error getting access token: {str(e)}")
            return None

    def send_message(self, message: str, touser: str = "@all") -> bool:
        """
        Send message to specified user(s)
        Args:
            message: Content to send
            touser: WeChat user ID(s), default "@all" for all users
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get fresh token if needed
            if not self.token:
                self.token = self.get_access_token()

            if not self.token:
                return False

            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.token}"

            data = {
                "touser": touser,
                "msgtype": "text",
                "agentid": self.agentid,
                "text": {"content": message},
            }

            response = requests.post(url, data=json.dumps(data))
            result = response.json()

            if result["errcode"] == 0:
                logging.info("Message sent successfully")
                return True
            else:
                logging.error(f"Failed to send message: {result}")
                return False

        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return False


def main():
    # Test the notification
    notifier = WeChatNotifier()

    # Test message
    test_message = "🧸 Test notification from Jellycat Stock Checker!"

    # Send test message
    success = notifier.send_message(test_message)
    print(f"Message sent: {'Success' if success else 'Failed'}")


if __name__ == "__main__":
    main()

"""
整体思路：
利用selenium+chrome driver调起chrome并访问discord的好友推荐页面
过滤出friend-suggestions的响应内容
"""
import json

from loguru import logger

from selenium_utils import get_driver
from settings import *

# /home/rhino/sns/dc/discord-crawler-YYYY-MM-DD_HH-mm-ss_ssssss.log
logger.add(os.path.join(DUMP_DIR, 'discord_crawler_{time:YYYYMMDD}.log'), rotation="50 MB", retention="3 days",
           compression="gz", enqueue=True)

driver = get_driver()

# 设置浏览器最大化，但是有时会导致该爬虫错误
driver.maximize_window()


def go(url):
    driver.get(url)

    logger.success('{} all done'.format(url))


def _get_log():
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    results = []

    for log in filter(
            lambda x:
            x['method'] == 'Network.responseReceived' and
            '/friend-suggestions' in x['params']['response']['url'],
            logs):
        try:
            request_id = log["params"]["requestId"]
            # 这里是响应内容
            results.append(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
        except Exception as s:
            logger.error(s)
            pass

    return results, logs


if __name__ == '__main__':
    try:
        go(CHANNEL_AT_ME)
    finally:
        driver.close()
        driver.quit()

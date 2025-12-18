"""
整体思路：
利用selenium+chrome driver调起chrome并访问discord的好友推荐页面
过滤出friend-suggestions的响应内容
"""
import json

from loguru import logger

from selenium_utils import get_driver, sleep
from settings import *

# /home/rhino/sns/dc/discord-crawler-YYYY-MM-DD_HH-mm-ss_ssssss.log
logger.add(os.path.join(DUMP_DIR, "discord_crawler_{time:YYYYMMDD}.log"), rotation="50 MB", retention="3 days",
           compression="gz", enqueue=True)

driver = get_driver()

# 设置浏览器最大化，但是有时会导致该爬虫错误
driver.maximize_window()


def go(url):
    driver.get(url)

    sleep(30)

    network_logs = _get_log()

    suggestions = process_network_logs(network_logs)

    filename = f"{TODAY}_{APP_TYPE}_suggestion.json"

    output_file = os.path.join(DUMP_DIR, filename)
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, "w", encoding="utf-8") as f:
        logger.debug("writing records to file")
        f.write(json.dumps(suggestions))

    logger.success(f"{APP_TYPE} suggestion friends all done")


def extract_suggestions(a_network_log):
    """
    从性能日志中抽好友推荐列表
    :param a_network_log:
    :return:
    """
    try:
        body = json.loads(a_network_log.get("body", ""))

        return body
    except (json.JSONDecodeError, KeyError):
        return []


def format_suggestion(a_suggestion):
    result = {}

    if a_suggestion.get("reasons", None):
        contact_info = a_suggestion.get("reasons")[0]
        # 指取推荐理由为通讯录的
        if contact_info and contact_info.get("platform_type", "") == "contacts":
            # 通讯录内的名称
            result.update({"contact_name": contact_info.get("name")})
            # 应用内的名称
            result.update({"username": a_suggestion.get("suggested_user", {}).get("username", '')})

    return result


def process_network_logs(network_logs):
    """
    处理性能日志
    :param network_logs:
    :return:
    """
    result = []
    for a_network_log in network_logs:
        suggestions = extract_suggestions(a_network_log)
        if suggestions:
            result.extend([format_suggestion(a_suggestion) for a_suggestion in suggestions])
    return result


def _get_log():
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    results = []

    for log in filter(
            lambda x:
            x["method"] == "Network.responseReceived" and
            "/friend-suggestions" in x["params"]["response"]["url"],
            logs):
        try:
            request_id = log["params"]["requestId"]
            # 这里是响应内容
            results.append(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
        except Exception as s:
            logger.error(s)
            pass

    return results


if __name__ == "__main__":
    try:
        go(CHANNEL_AT_ME)
    finally:
        driver.close()
        driver.quit()

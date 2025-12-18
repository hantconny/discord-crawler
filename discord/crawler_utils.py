# -*- coding:utf-8 -*-
import time

import requests
from loguru import logger
from tqdm import tqdm

from selenium_utils import sleep


def get_local_time(utc_ts_):
    """
    返回当地时间，而不是UTC时间
    :param utc_ts_:
    :return:
    """
    local_struct_time = time.localtime(utc_ts_)
    return time.strftime('%Y-%m-%d %H:%M:%S', local_struct_time)


def make_requests(url):
    # 猜测出现备选列表时批量请求头像太过集中并发导致被 CDN 断开
    # 每个请求间停顿 5 秒，解决服务端主动断开的问题
    sleep(5)

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,lo;q=0.6",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    retry = 0
    max_retry = 3

    while retry < max_retry:
        try:
            resp = requests.get(url, headers=headers, timeout=(5, 5))
            return resp
        except Exception as e:
            # 出现异常时进行长等待
            retry += 1
            logger.error(f"requests 请求 {url} 第 {retry} 次失败: {e}，1分钟后重试")
            for _ in tqdm(range(1 * 60), desc="请求重试", unit="s"):
                sleep(1)

    # 多次等待无果则返回空响应
    response = requests.Response()
    response._content = b'EMPTY'  # 注意：这是受保护属性，必须是字节串 bytes
    return response

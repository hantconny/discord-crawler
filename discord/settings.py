import os.path
import time

"""
命名规则为/home/rhino/{project}/{sub-proj}
project可选值为: ip, sns, tor
sub-proj可选值为: 
  ip: v4, v6
  sns: fb, tw, ut, ins, tk, vk, dc
  tor: 直接存放
"""
DUMP_DIR = '/home/rhino/sns/dc'
if not os.path.exists(DUMP_DIR):
    os.makedirs(DUMP_DIR)

# 20231202
TODAY = time.strftime('%Y%m%d', time.localtime())
# Chrome测试版解压位置，不要与客户机使用相同的Chrome
CHROME_TEST = 'D:/ENV/chromedriver/chrome-win64/chrome.exe'
# 保存登录信息，指定为一个非用户使用Chrome的目录，一般指定在爬虫输出目录同级
CHROME_USER_DATA_DIR = 'D:/home/rhino/chrome'
# 保存登录 cookies，共立即爬取使用
CHROME_USER_COOKIES = 'D:/home/rhino/chrome/dc_saved_cookies.json'

# 不再需要该配置，海外无需代理，国内即使不配置浏览器和requests也走会系统代理
# PROXY_ENABLED = True
# HTTP_PROXY = 'http://127.0.0.1:7890'

RETRY_LIMIT = 1
# 向下滚动的次数
SCROLL_LIMIT = 5

LOGIN = True

INCOGNITO = False

CHANNEL_AT_ME = 'https://discord.com/channels/@me'

# OWLS设控文件输出目录 20240102.text
OWLS_TARGET_DIR = 'D:/home/rhino/snsMapping/accountInfo'

APP_TYPE = 'discord'

# 配合主动任务脚本 follow.py 执行添加好友
# 将 CRAWLER_ID 作为索引，到设控文件 yyyymmdd_follow.txt 中的 interval 字段中取 sleep 时间作为延迟
# 不同主机部署的爬虫脚本 CRAWLER_ID 应不一样
CRAWLER_ID = 0
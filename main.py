import requests
import datetime
import re
import os
from dingtalkchatbot.chatbot import DingtalkChatbot



keywords =os.environ["keywords"]
webhook=os.environ["webhook"]
secretKey=os.environ["secretKey"]
github_token = '11'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def splitKeywordList():
    return keywords.split()

def dingding(text, msg,webhook,secretKey):
    ding = DingtalkChatbot(webhook, secret=secretKey)
    ding.send_text(msg='{}\r\n{}'.format(text, msg), is_at_all=False)


def sendmsg(keyword,pushdata):
    text=""
    for data in pushdata:
        text+="工具名称:{}\n工具网址:{}\n详情:{}\n\n\n ".format(data.get("keyword_name"),data.get("keyword_url"),data.get("description"))
    dingding("关键字："+keyword,text,webhook,secretKey)



def getKeywordNews(keyword):
    today_keyword_info_tmp=[]
    try:
        # 抓取本年的
        api = "https://api.github.com/search/repositories?q={}&sort=updated".format(keyword)
        json_str = requests.get(api, timeout=10).json()
        # today_date = datetime.date.today()
        today_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        n=20 if len(json_str['items'])>20 else len(json_str['items'])
        for i in range(0, n):
            keyword_url = json_str['items'][i]['html_url']
            try:
                keyword_name = json_str['items'][i]['name']
                description=json_str['items'][i]['description']
                pushed_at_tmp = json_str['items'][i]['pushed_at']
                pushed_at = re.findall('\d{4}-\d{2}-\d{2}', pushed_at_tmp)[0]
                if pushed_at == str(today_date):
                    today_keyword_info_tmp.append({"keyword_name": keyword_name, "keyword_url": keyword_url, "pushed_at": pushed_at,"description":description})
                    print("[+] keyword: {} ,{} ,{} ,{} ,{}".format(keyword, keyword_name,keyword_url,pushed_at,description))
                else:
                    print("[-] keyword: {} ,{}的更新时间为{}, 不属于今天".format(keyword, keyword_name, pushed_at))
            except Exception as e:
                pass
    except Exception as e:
        print("github链接不通")
    return today_keyword_info_tmp

def getPushList(keywords_list):

    try:
        for item in keywords_list:
            retList=getKeywordNews(item)
            sendmsg(item,retList)

    except Exception as e:
        print("getpush exception")

if __name__ == '__main__':
    keywords_list =splitKeywordList()
    print(keywords_list)
    getPushList(keywords_list)


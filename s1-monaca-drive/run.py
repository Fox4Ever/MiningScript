import time
import json
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from queue import Queue


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_driver = "./chromedriver"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

domain = "https://monaconft.io/"

fo_cache = {}

with open("./fo_cache.json") as f:
    fo_cache = json.load(f)

def write_to_file():
    with open("./fo_cache.json", 'w') as f:
        json.dump(fo_cache, f, ensure_ascii=True, indent=4, sort_keys=True)

def my_random(x, y):
    return random.randint(x, y)


def to_follow(user_id, retry = False):
    driver.get(domain + user_id)
    time.sleep(my_random(8, 18))
    try: 
        fo_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/div/div/div[3]/div[1]/div[4]/div[2]')
        fo_button_text = fo_button.text.strip().lower()
        if fo_button_text == "unfollow":
            print(f'- [DEV] [{user_id}] 已经 follow，无需其他操作')
            fo_cache[user_id] = True
            write_to_file()
        else:
            ActionChains(driver).move_to_element(fo_button).click().perform()
            print(f'- [DEV] [{user_id}] follow 完成 ✅')
            fo_cache[user_id] = True
            time.sleep(5)
            write_to_file()
            return True
    except:
        print(f"- [DEV] [{user_id}] 关注失败")
        if retry:
            print("- [DEV] 8s 后继续尝试")
            time.sleep(8)
            to_follow(user_id)
        else:
            print("- [DEV] 继续关注下一个")
        return False

def get_following_users(user_id):
    try: 
        api_uri = f'https://api.monaconft.io/api/user/getFollowingList?uid={user_id}'
        driver.get(api_uri)
        time.sleep(my_random(5, 10))
        follow_list = driver.find_element_by_xpath('/html/body/pre').text
        obj = json.loads(follow_list)
        if isinstance(obj, dict) and 'data' in obj:
            if isinstance(obj['data'], list) and len(obj) > 0:
                return list(map(lambda x: x['uid'], obj['data']))
        return []
    except:
        return []


def main():
    tot_cnt = 0
    # 任务队列
    task_que = Queue()

    # 初始化队列
    st_user = "jxj_nft"
    task_que.put(st_user)

    while task_que.qsize() > 0:
        cur_user = task_que.get()

        print(f'- [DEV] 处理用户 {cur_user}')
        
        # 先关注一下这个人
        isSuccess = to_follow(user_id=cur_user)
        if isSuccess:
            tot_cnt += 1
            print(f'- [DEV] 成功关注 {tot_cnt} 人')

        # 获取这个人的关注列表
        follower_list = get_following_users(user_id=cur_user)
        new_users = []

        # 去重入队
        for nxt_user in follower_list:
            if nxt_user in fo_cache:
                continue
            task_que.put(nxt_user)
            new_users.append(nxt_user)

        print(f'- [DEV] 新增用户 {new_users}')

        # 检查队列是否过大，造成 OOM
        while task_que.qsize() > 100:
            pre_cur_user = task_que.get()
            if pre_cur_user in fo_cache:
                continue
            print(f'- [DEV] 处理用户 {pre_cur_user}')
            isSuccess = to_follow(user_id=pre_cur_user)
            if isSuccess:
                tot_cnt += 1
                print(f'- [DEV] 成功关注 {tot_cnt} 人')
            


main()

# 主流币种名字
# f = open('./tokens.json')
# data = json.load(f)

# for tt in data['marketCapData']:
#     try:
#         sym = tt['symbol']``
#         to_follow(user_id=sym)
#     except: 
#         continue

# words = "abcdefghijklmnopqrstuvwxyz"
# numbers = "1234567890"

# for a in words:
#     for b in numbers:
#         user_id = a + b
#         to_follow(user_id=user_id)
#         time.sleep(8)



# 连字母 连续数
# for i in "klmnopqrstuvwxyz":
#     meta_user_id = f'{i}'
#     for j in range(0, 5):
#         user_id = ""
#         for k in range(0, j):
#             user_id += meta_user_id
#         if user_id == "":
#             continue
#         to_follow(user_id=user_id)    
#         time.sleep(8)
    
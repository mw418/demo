import sys
import time
import hashlib
import requests
import urllib3
import threading
from fake_useragent import UserAgent
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
locks = threading.Lock()

orderno = "" #订单号
secret = ""  #密钥
ip = "forward.xdaili.cn"
port = "80"
ip_port = ip + ":" + port
count = 0
def getresponse( url):
    timestamp = str(int(time.time()))
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    string = string.encode()
    md5_string = hashlib.md5(string).hexdigest()
    sign = md5_string.upper()
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": auth, "User-Agent": UserAgent().random, 'Connection': 'close'}
    global count
    while True:
        try:
            s = requests.session()
            s.keep_alive = False
            r = s.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        except Exception as e:
            print(e)
            print(f'{count+1}出错')
            time.sleep(2)
            continue
        r.encoding = 'utf8'
        if r.ok:
            with locks:
                if count >= 5:
                    break
                count += 1
                print(f"{count}次")
            time.sleep(0.2)
        r.close()
if __name__ == '__main__':
    url = 'https://www.93book.com/?fromuid=511549'
    list1=[]
    for i in range(7):
        list1.append(threading.Thread(target=getresponse, args=(url,)))
    for i in list1:
        i.start()
    for i in list1:
        i.join()



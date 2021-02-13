import requests
import re
import os

def geturl_text(url):
    #这个网站是gbk的
    gethtml=requests.get(url)
    return str(gethtml.content,"gbk")
def getstr_mid(s,left,right):
    #取出左右str中间的字符串
    return s[s.find(left)+len(left):s.find(right)]
headers={"Referer":"https://www.mm131.net/xinggan/"}#用于请求的消息头，不然会失败
#======================================================
#图片官网：https://www.mm131.net/
url=input("请输入地址：")#第一张图片的地址
#url="http://www.mm131.net/xinggan/5734_2.html"
text=geturl_text(url)
page=re.search('<span class="page-ch">共.*页</span>',text).group(0)
page=getstr_mid(page,"共","页")
title=re.search('<h5>.*</h5>',text).group(0)
title=getstr_mid(title,"<h5>","</h5>")
print("标题：",title)
print("页数：",page)

if not os.path.exists("./"+title):
    #在当前目录创建目录
    os.mkdir("./"+title)
    print("创建目录 "+title)
for i in range(1,int(page)+1):
    print("正在下载：%d/%s"%(i,page))
    text=geturl_text(url) #读取内容
    pic_url=re.search('<div class="content-pic">.*src=".* /',text).group(0)
    pic_url=getstr_mid(pic_url.replace('"',""),'src=',' /')#取出图片地址
    print(pic_url)

    with open("./"+title+"/"+str(i)+".jpg","wb") as f:
        f.write(requests.get(pic_url,headers=headers).content)
        print("success!")
    next_url=re.search('<div class="content-pic"><a href=".*\.html">',text).group(0)
    next_url=next_url[next_url.rfind('href="')+6:-2] #取出下一页地址，如 4647_2.html
    url=url.replace(url[url.rfind("/")+1:],next_url) #倒找/xxx.html，替换为下一页的地址
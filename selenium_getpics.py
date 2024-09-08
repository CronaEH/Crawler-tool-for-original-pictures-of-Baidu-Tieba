#导入库
from selenium import webdriver#注意文件名不能是selenium.py，否则和模块名同名，导致错误：cannot import name 'webdriver' from partially initialized module 'selenium'
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
import requests
import json
#设置工作目录为py文件所在路径
os.chdir(os.path.dirname(__file__))
#打开config.json
with open("config.json",encoding='utf8') as json_file:
    config = json.load(json_file)
chrome_driver_path = config['driver_path']
chrome_driver_path = "C:\\Program Files\\Google\\Chrome\\chromedriver-win64\\chromedriver.exe" # 设置 ChromeDriver 的路径
#打开驱动
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument("--headless")
driver = webdriver.Chrome(service=service,options=options)
# 获取目标连接
#url_src = 'https://tieba.baidu.com/p/6181195541?'  # 替换为你想爬取的贴吧链接
while 1:
    url_src = input("请输入网址(格式为https://tieba.baidu.com/p/帖子编号?(记得加上?)):")
    if re.match( r'https://tieba.baidu.com/p/\d*\?', url_src):
        break
    else:
        print("格式错误")
all_flag = input('是否要全部抓取?输入0为默认全部抓取,输入其他为展示页面信息后再决定抓取:')
driver.get(url_src)
# 等待页面加载
time.sleep(3)  # 根据网络情况调整等待时间
# 获取网页源代码
page_source = driver.page_source
#获取网页页数
page_format='<a href="/p/\d+\?pn=(\d*)">尾页</a>'
page_r=re.compile(page_format)
if re.search(page_r, page_source):
    page_num=eval(re.findall(page_r, page_source)[0])
else:
    page_num=1
#获取帖子名
name_format='class\="core_title_txt pull-left text-overflow  " title\="([^\x00-\x1F\x7F-\x9F]*?)"'
name_r = re.compile(name_format)
name = re.findall(name_r, page_source)[0]
#获取源图编号
pic_format = r'<img class="BDE_Image".*? src="(.*?)".*?>'#r让字符串中的\被视为普通字符
pic_r = re.compile(pic_format)  
pic_src_format=r'sign=\w*/(\w*.jpg)'
pic_src_r=re.compile(pic_src_format)
image_all=[]
image_type = []
for page in range(page_num):
    image_all.append([])
    image_type.append([])
    url = url_src+'pn='+str(page+1)
    driver.get(url)
    time.sleep(1)
    print("获得第{}页源代码".format(page+1))
    #所有预览图地址
    page_source = driver.page_source
    pic_web = re.findall(pic_r, page_source)
    for tar in pic_web:
        if 'https://imgsa' in tar:
            image_type[page].append('0')
            image_all[page].append(re.findall(pic_src_r,tar)[0])
        else:
            image_type[page].append('1')
            image_all[page].append(tar)
        
# 关闭浏览器
driver.quit()
#统计图片
pic_nums_per=list(map(lambda x: len(x),image_all))#统计每个子数组的长度
#print(image_all)
print('该帖子一共有{}页，共发现 {}张图片，其中:'.format(page_num,sum(pic_nums_per)))
for i in range(page_num):
    print('第{}页共有{}张图片'.format(i+1,pic_nums_per[i]))
#设置页数
if all_flag == '0':
    print('保存所有页码')
    page_need=[i+1 for i in range(page_num)]
else:
    in_format=r'\d+'#r让字符串中的\被视为普通字符
    in_r = re.compile(in_format)  
    in_flag=0
    print('网页共{}页'.format(page_num))
    page_need=[]
    while in_flag==0:
        enter=input('请输入你要保存的页码，0为全部保存')
        target = re.findall(in_r,enter)
        if len(target)==1 and target[0]=='0':
            print('保存所有页码')
            page_need=[i+1 for i in range(page_num)]
            in_flag=1
        elif len(target)== 0:
            print('输入错误，重新输入')
        else:
            in_flag=1
            for i in target:
                if eval(i)>page_num or eval(i)==0:
                    print('页码错误，重新输入')
                    page_need.clear()
                    in_flag = 0
                    break
                page_need.append(eval(i))

#保存图片 
src_prefix1='https://imgsa.baidu.com/forum/pic/item/'#原图前缀+预览图网址sign后的内容就是原图网址
output=config['save_path']
if not os.path.exists(output+name):
    os.mkdir(output+name)

for i in page_need:
    print('开始下载第{}页:'.format(i))
    page_loc=output+name+'\\第'+str(i)+'页(共'+str(pic_nums_per[i-1])+'张)'
    if not os.path.exists(page_loc):
        os.mkdir(page_loc)
    for j,tar in enumerate(image_all[i-1]):
        if image_type[i-1][j] == '0':
            pic_loc=src_prefix1+tar
        else:
            pic_loc=tar
        response = requests.get(pic_loc)
        if response.status_code == 200:
            with open(page_loc+'\\'+str(j+1)+'.jpg', 'wb') as file:
                file.write(response.content)
                print('图片已成功下载并保存为{}'.format(page_loc+'\\'+str(j+1)+'.jpg'))
        else:
            print("下载失败，状态码: {response.status_code}")



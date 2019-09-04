import pandas as pd
import numpy as np
import re
import requests
import json
import os
import urllib
import requests
import time
import random
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

os.chdir('F:/005_Works/CV/scraper/boss')

page_headers={
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
         'Connection':'keep-alive',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Host':'www.zhipin.com',
         'Accept-Language':'zh-CN,zh;q=0.8',
         'Cache-Control':'max-age=0',
         'Referer':'https://www.zhipin.com/',
         'Upgrade-Insecure-Requests':'1',
         'cookie': '__g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1567482282; t=BGdp047GahnpgnZh; wt=BGdp047GahnpgnZh; __c=1567482315; _bl_uid=s6kwj0y13dgaapiy12a8n02aFUzt; __l=r=https%3A%2F%2Flogin.zhipin.com%2F&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Frecommend&friend_source=0&friend_source=0; __zp_stoken__=c688%2BO0o50rwIib5ASNxKoBXXsAk77sOHv0RWcsge4rf2WPFi%2B1S%2BBCrlMsh%2Bc%2BDDpVjHARzpnUt67gRaXyrl01cvg%3D%3D; __a=24515062.1567482278.1567482278.1567482315.9.2.8.9; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1567517487'

         }
proxies = {
    "http":'http://111.231.140.109:8888'
}

#设置搜索职位名称
key_words = "数据分析"
key = urllib.parse.quote(key_words)

# 获取页面（一级页、二级页）内容
def get_data(url):
    try:
        res=requests.get(url,headers=page_headers, proxies = proxies)
        status=res.status_code
        data=res.content.decode('UTF-8')
        print(status)
        soup=BeautifulSoup(data,'lxml')
        return soup,status

    except Exception as e:
        print(str(e))
        return 0,0


# 获取每个职位的详细信息（工作描述、岗位职责）
def get_details(url):
    soup,status=get_data(url)
    if status==200:
        job_detail=soup.find('div',class_="job-sec")
        try:
            details = job_detail.find('div', class_ = 'text').text
            details = details.replace('\r\n',"").replace(',',"，").strip()
            return details
        except Exception as e:
            print(str(e))
            

def get_job(url):
    soup,status=get_data(url)
    if status==200:
        job_all=soup.find_all('div',class_="job-primary")
        for job in job_all:
            try:
                #职位名
                job_title=job.find('div',class_="job-title").string
                #薪资
                job_salary=job.find('span',class_="red").string
                #职位标签
                job_tag1=job.p.text
                #公司
                job_company=job.find('div',class_="company-text").a.text
                #招聘详情页链接
                job_url=job.find('div',class_="info-primary").a.attrs['href']
                job_url = "https://www.zhipin.com" + job_url

                job_detail = get_details(job_url)
                #公司标签
                job_tag2=job.find('div',class_="company-text").p.text
                #发布时间
                job_time=job.find('div',class_="info-publis").p.text
                
                with open('job.csv','a+',encoding='GB18030') as fh:
                    fh.write(job_company+","+job_title+","+job_salary+","+job_tag1+","+job_time+","+job_tag2+","+job_url+","+job_detail+"\n")
            except Exception as e:
                print(str(e))

if __name__=='__main__':
    with open('job.csv','w',encoding='GB18030') as fh:
        fh.write("公司,职位名,薪资,职位标签,发布时间,公司标签,招聘链接,岗位要求\n")
    for i in range(1,20):
        print("正在爬取第 %s 页..." % i)
        url='https://www.zhipin.com/c101280600/?query='+key+'&page='+str(i)+'&ka=page-'+str(i)
        get_job(url)
        #随机等待
        span=round(random.random()*6,1)
        time.sleep(span)
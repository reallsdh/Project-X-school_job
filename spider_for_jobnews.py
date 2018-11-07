# -*- coding: utf8 -*-

"""sprider for school_job_information_V1.1
   爬的是当前日期之后的宣讲会信息
   返回的字段[公司，宣讲会地点，举办学校，详细链接，举办时间]
   会在代码路径下生成以当前日期命名的结果文件
   涉及高校[nuaa/seu...]
"""

import requests
from bs4 import BeautifulSoup
import time

##获得总页数
def getPages(url):
    soup = gethtml(url)
    totalpage = soup.select('span.orange')[0].text
    return totalpage

def gethtml(url):
    # html = 'http://nuaa.91job.gov.cn/teachin/index?page=1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    data = requests.get(url, headers=headers)
    data.raise_for_status()
    data.encoding = data.apparent_encoding
    c = data.text
    soup = BeautifulSoup(c, 'lxml')
    return soup


def getinfo(url,jobinfo):
    totalpage = getPages(url)
    nowaday_time = time.strftime("%Y-%m-%d", time.localtime())
    status = 'on' #标志位
    for i in range(1,int(totalpage)+1):
        newurl = url.split('=')[0]+'='+ str(i)
        print('spider page:',i)
        time.sleep(3)  #sleep for a while
        soup = gethtml(newurl)
        li1 = soup.find_all('ul',class_= ['infoList teachinList'])
        for arr in li1:
            jobname = arr.select('li.span1')[0].text.strip('\n')
            jobschool = arr.select('li.span5')[0].text
            jobroom = arr.select('li.span4')[0].text
            jobdetails = url.split('/teachin')[0] + arr.find_all('a')[0]['href'] #招聘详细信息地址
            jobtime = arr.select('li.span5')[1].text
            if jobtime.split('\t')[0] < nowaday_time: #只需要当前时间节点之后的宣讲会信息
                status = 'off'
                break
            else:
                jobinfo.append([jobname+'\t',jobroom+'\t',jobschool+'\t',jobdetails+'\t',jobtime+'\n'])
            write_to_csv(jobinfo)
            jobinfo =[]
        if status =='off':
            break

def get_school_name(): #可以维护一个高校就业网的库
    school_list = ['nuaa','seu','njust','nju','njupt','hhu']
    return school_list


def write_to_csv(content=[]):
    time_sub = time.strftime("%Y-%m-%d", time.localtime())
    with open(u'job_information_'+time_sub+'.txt','a',encoding='utf8') as w:
        for cc in content:
            for dd in cc:
          w.writelines(dd)


if __name__ == '__main__':
    school_name = get_school_name()
    nowaday_time = time.strftime("%Y-%m-%d", time.localtime())
    print ('Today is :',nowaday_time)
    jobinfo =[]
    headers =[u'公司名\t',u'宣讲会地址\t',u'学校\t',u'详细链接\t',u'宣讲会时间\n']
    jobinfo.append(headers)
    for name in school_name:
        url = 'http://' + name + '.91job.gov.cn/teachin/index?page=1'
        print ('Now crawling：',url.split('/teachin')[0])
        try:
            getPages(url)
            getinfo(url,jobinfo)
        except:
            print (name,'Connection Error，Please Click:',url)


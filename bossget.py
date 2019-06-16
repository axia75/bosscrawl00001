import urllib.request
from bs4 import BeautifulSoup
import ssl
import urllib.parse
from lxml import etree 
import re
import time

def get_html(url):
    context = ssl._create_unverified_context()     
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req,context=context)
    html = res.read().decode('UTF-8')
    return html
 

def saveHtml(htmc,icount):
    
    getbhtml = './html/test%d'%(icount)+'.html' 
    #打开文件，准备写入
    f = open(getbhtml,'wb')   
    #time.sleep(2) # 保证浏览器响应成功后再进行下一步操作
    #写入文件
    f.write(htmc.encode("UTF-8", "ignore")) # 忽略非法字符
    print('写入成功')
    #关闭文件
    f.close() 

def saveJobdetail(htmc,icount):
    
    getDetail = './html/data/jd%d'%(icount)+'.txt' 
    #打开文件，准备写入
    with open(getDetail,'a')   as f:
        f.write(htmc) # 忽略非法字符
        print('写入成功')
        #关闭文件
        f.close()     

def catchJoblist():    
#if __name__=="__main__":
    # 生成证书上下文(unverified 就是不验证https证书)
           
        icount = 1
        #html = urlopen("https://www.zhipin.com/c101010100/?ka=open_joblist", context=context)
        html = get_html("https://www.zhipin.com/c101010100/y_7/?period=4&ka=sel-salary-7")
        #bsObj = BeautifulSoup(html)            
        saveHtml(html,icount)
        while icount < 11: 
            icount += 1
            #html = urlopen('https://www.zhipin.com/c101010100/?page=%s&ka=page-next'%icount, context=context)   
            html = get_html('https://www.zhipin.com/c101010100/y_7/?period=4&page=%s&ka=page-next'%icount)         
            saveHtml(html,icount)

def readHtml():
    icount = 1
    while icount < 11: 
        getbhtml = './html/test%d'%(icount)+'.html'        
        icount += 1       
        with open(getbhtml,encoding="utf8") as f:
            bsObj = BeautifulSoup(f.read())         
            #joblist = bsObj.findAll("div", {"class":"job-primary"})
            for k in bsObj.find_all('a'):
                #try：                      
                    if k.get('data-jid'):
                        pass
                    else:
                       continue
                    if k.get('data-jobid'):
                        pass
                    else:
                        continue
                    if k.get('href'):  
                       vsr = "dddd" # k['href'] 
                       time.sleep(2) # 保证浏览器响应成功后再进行下一步操作
                       htmls = get_html('https://www.zhipin.com'+k['href'] )   
                       #saveHtml(htmls,13)
                       detObj = BeautifulSoup(htmls)   
                       names = detObj.find("div", {"class":"name"})
                       name = ''
                       if names is not None:
                          name = names.get_text()
                          #print(name)
                          #saveJobdetail(name,icount)
                       sall  = detObj.find("span", {"class":"badge"}) 
                       sal = ''
                       if sall is not None:
                          sal = sall.get_text()
                          #saveJobdetail(sal,icount)
                       jdintr = detObj.findAll("div", {"class":"text"})
                       contnetss = jdintr[0].contents
                       #print(contnetss[0])
                       #print(contnetss[1])
                       textss = jdintr[0].get_text()
                       #print(jdintr[0].get_text())

                       textp = name +"\n\r"+sal+"\n\r"+textss

                       saveJobdetail(textss,icount)
                #except ZeroDivisionError as e:
                    #print('发生了异常：',e)

if __name__=="__main__":  
    readHtml()
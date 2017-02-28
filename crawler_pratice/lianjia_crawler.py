# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 13:59:06 2017

@author: bal
"""

import urllib3
from bs4 import BeautifulSoup as bs
import csv



page_num = 1
start_url = "http://sh.lianjia.com/ershoufang/d"

def get_page_contents(host_url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    data = urllib3.PoolManager().request("POST",host_url).data
    return data
def parser_page(html):
#    global page_num
    soup = bs(html,"html.parser")
    house_mes = soup.find('ul',attrs={'id':'house-lst','class':'house-lst'})
    res_list = []
    house_list = []
    for li in house_mes.find_all('li'):
        detail = li.find('div',attrs={'class':'info-panel'})
        
        house_price = detail.find('span',attrs = {'class':'num'}).getText()
        
        house_detail = li.find('div',attrs={'class':'where'})
        
        house_size = house_detail.find('a',attrs={'class':'laisuzhou'}).find_next_siblings("span")[1].getText()
        
        house_style = house_detail.find('a',attrs={'class':'laisuzhou'}).find_next_siblings("span")[0].getText()
        
        house_addr = house_detail.find('span',attrs={'class':'nameEllipsis'}).getText()
        
        house_price_pre = detail.find('div',attrs={'class':'price-pre'}).getText()
        
        house_direction = detail.find('div',attrs={'class':'con'}).getText()[1:3]
                                      
        house_lvl = detail.find('div',attrs={'class':'con'}).getText()[9:11]
        
        house_build_year = detail.find('div',attrs={'class':'con'}).getText()[-25:-1]
                                       
        house_h = detail.find('div',attrs={'class':'con'}).getText()[5:8]
                              
        if house_build_year.isspace():
            house_build_year = 1
        else:                               
            house_build_year = house_build_year.split('年建')[0]
                               
        house_size = house_size.split()[0]
        house_style = house_style.split()[0]
        house_lvl = house_lvl.split('层')[0]
        house_price_pre = house_price_pre.split('元')[0]

        house_list = [
                      house_addr,
                      house_direction,
                      house_h,
                      house_lvl,
                      house_build_year,
                      house_size,house_style,
                      house_price,house_price_pre
                      ]
        res_list.append(house_list)
    return res_list    
#        print( house_addr,house_price+'万',house_size,house_style)
        
def main():        
    with open('test.csv','w') as f:
        wr = csv.writer(f)
        for i in range(1,3133):
            global page_num
            page_num += 1   
            host_url = start_url + str(page_num)
            html = get_page_contents(host_url)
            res = parser_page(html)
            print(page_num)
            for item in res:
                wr.writerow(item)
    f.close()
        
if __name__ =='__main__':
    main()

    
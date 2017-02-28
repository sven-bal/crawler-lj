# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 22:26:08 2017

@author: bal
"""

import pandas
import numpy as np
import pygal
from pygal import style

def get_block(f):
#获取各行政区的售房总数
    block_count = f['block'].value_counts().to_dict()
    d_block_count = {}
    for k,v in block_count.items():
        d_block_count[v] = k
    return d_block_count#sorted(d_block_count.keys()),[d_block_count[i] for i in sorted(d_block_count.keys())]#

def get_name(f):
#获取在售小区的出售房数量
    name_count = f['name'].value_counts()[0:15].to_dict()
    d_name_count = {}
    for k,v in name_count.items():
        d_name_count[v] = k
    return d_name_count#sorted(d_name_count.keys()),[d_name_count[i] for i in sorted(d_name_count.keys())]#

def get_size(f):
#获取各面积区间内出售房总数
    d_size = {}
    index1 = f['size']>=500
    index2 = (f['size']<500)&(f['size']>=250)
    index3 =(f['size']<250)&(f['size']>=150)
    index4 = (f['size']<150)&(f['size']>=95)
    index5 = (f['size']<95)&(f['size']>=75)
    index6 = (f['size']<75)&(f['size']>=45)
    index7 = f['size']<45
    l_index = [index1,index2,index3,index4,index5,index6,index7]
    
    k = ['大于500平方','250至500平方','150至250平方','95至150平方','75至95平方','45至75平方','小于45平方']            
    for i in range(len(l_index)):
        d_size[len(f[l_index[i]])]=k[i]
    return d_size#sorted(d_size.keys()),[d_size[i] for i in sorted(d_size.keys())]#
    
def get_size_pre_price(f):
    d_size_pre_price = {}
    index1 = f['size']>=500
    index2 = (f['size']<500)&(f['size']>=250)
    index3 =(f['size']<250)&(f['size']>=150)
    index4 = (f['size']<150)&(f['size']>=95)
    index5 = (f['size']<95)&(f['size']>=75)
    index6 = (f['size']<75)&(f['size']>=45)
    index7 = f['size']<45
    l_index = [index1,index2,index3,index4,index5,index6,index7]
    
    k = ['大于500平方','250至500平方','150至250平方','95至150平方','75至95平方','45至75平方','小于45平方']
    for i in range(len(l_index)):
                    
#        print(np.average(f[l_index[i]]['pre_price']))
        d_size_pre_price[int(np.average(f[l_index[i]]['pre_price']))] = k[i]
    return d_size_pre_price#sorted(d_size_pre_price.keys()),[d_size_pre_price[i] for i in sorted(d_size_pre_price.keys())]#
    
def get_block_pre(f):
#获取各行政区每平米房价中值、平均值    
    d_block_pre = {}
    l_block =  f['block'].value_counts().keys().drop('上海')
    for i in l_block:       
        pre_price = np.average(f[f['block']==i]['pre_price'])       
        d_block_pre[int(pre_price)] = i
    return d_block_pre#sorted(d_block_pre.keys()),[d_block_pre[i] for i in sorted(d_block_pre.keys())]#

def get_price_median(f):
    l_block =  f['block'].value_counts().keys().drop('上海')
    d_block_median = {}
    for i in l_block:
        median_price = np.median(f[f['block']==i]['pre_price'])
        d_block_median[int(median_price)] = i
    return d_block_median #sorted(d_block_median.keys()),[d_block_median[i] for i in sorted(d_block_median.keys())]#

def get_size_sum(f):
    d_size_sum = {}
    l_block =  f['block'].value_counts().keys().drop('上海')
    for i in l_block:
        size_sum = np.sum(f[f['block']==i]['size'])
        d_size_sum[int(size_sum)] = i
    return d_size_sum
    #sorted(d_size_sum.keys()),[d_size_sum[i] for i in sorted(d_size_sum.keys())]
    
def get_price(f):
#获取各阶梯价格间在售房数量
    d_price = {}
    for i in range(11):
        l_k = []
        l_k.append(str(i)+'--'+str(i+1))
        for k in l_k:
            index = (f['price']<=(i+1)*100)&(f['price']>i*100)
            price = f[index]
            d_price[len(price)] = k
    price_max_count = len(f[(f['price']>1100)])
    d_price[price_max_count] = '>1100'        
    return d_price#sorted(d_price.keys()),[d_price[i] for i in sorted(d_price.keys())]#

    
def output_chart_size(res_size_price,res_size):
    style_chart1 = style.Style(colors=('#27e5e5','#000099',),background='white',plot_background='rgb(250,250,250)', value_font_size=14)
    chart_1 = pygal.Bar(title=str('上海在售二手房'),style=style_chart1,print_values=True, print_values_position='top',spacing=100,x_label_rotation=20)
    l = []
    ll = []
    sec = {}
    for k in sorted(list(res_size_price.keys())):
        l.append(res_size_price[k])     
    chart_1.x_labels=l 
    chart_1.add(str('每平米价格：元'),sorted(list(res_size_price.keys())))
    for k,v in res_size.items():
        sec[v] = k
    for i in l:
        ll.append(sec[i])
    chart_1.add('在售数量：套',ll)
    chart_1.render_to_file('面积.svg')

    
def output_chart_block(res_size_sum):
    style_block = style.Style(colors=('#27e5e5',),background='white',plot_background='rgb(250,250,250)', value_font_size=8)
    chart_1 = pygal.Bar(title='上海各区域在售二手房面积:百平方',print_values=True, style=style_block, spacing=50,x_label_rotation=20)
    l = []
    ll = []
    for k in sorted(list(res_size_sum.keys())):
        l.append(res_size_sum[k])    
        ll.append(int(k/100))
    chart_1.x_labels=l 
    chart_1.add(None,ll)
    chart_1.render_to_file('区域在售面积.svg')

def output_chart_tree(res_size_sum):
    style_tree = style.Style()
    chart = pygal.Treemap(title='区域在售面积:百平方',print_values=True,style=style_tree)
    l = []
    ll = []
    for k in sorted(list(res_size_sum.keys())):
        l.append(res_size_sum[k]) 
        ll.append(int(k/100))      
    for i in range(len(l)):
        chart.add(str(l[i]),ll[i])
    chart.render_to_file('tree.svg')
    
def output_chart_block2(res_block,res_price_median,res_block_pre):
    color = ('#007fff','#ff033e','#008000','#9966cc',)
    style_block = style.Style(colors=color,background='white',plot_background='rgb(250,250,250)', value_font_size=8)
    title = u'上海市在售二手房价格统计'
    chart = pygal.Bar(title=title,style=style_block,print_values=True,print_values_position = 'top',spacing=50)
    l_pre = sorted(res_block_pre.keys())
    x_lable =[]
    l_med = []
    l_num = []
    d1={}
    d2={}
    for i in l_pre:
        x_lable.append(res_block_pre[i])
    for k,v in res_block.items():
        d1[v]=k
    for k,v in res_price_median.items():
        d2[v]=k
    for i in x_lable:
        l_num.append(d1[i])
        l_med.append(d2[i])
    chart.x_labels=x_lable
    chart.add('价格均值：万元',l_pre)
    chart.add('价格中值：万元',l_med)
    chart.add('在售数量：套',l_num)

    chart.render_to_file('上海在售二手房价格.svg')
#    chart.x_labels=l
    
    
    
def main():
    f = pandas.read_csv('sh_lianjia.csv',encoding='gbk',sep=',',low_memory=False)
    res_price = get_price(f)
    res_name = get_name(f)
    res_block = get_block(f)
    res_size = get_size(f)
    res_block_pre = get_block_pre(f)
    res_price_median = get_price_median(f)
    res_size_sum = get_size_sum(f)
    res_size_price = get_size_pre_price(f)
#    output_chart_size(res_size_price,res_size)
#    output_chart_block(res_size_sum)
#    output_chart_tree(res_size_sum)
    output_chart_block2(res_block,res_price_median,res_block_pre)

    print('价格区间内在售数量：',res_price)
    print('---------------->>>>>')
    print('各面积区间内每平米价格均值：',res_size_price)
    print('---------------->>>>>')
    print('各面积区间内在售房数量：',res_size)
    print('---------------->>>>>')
    print('挂牌前15的小区：',res_name)
    print('---------------->>>>>')
    print('各大区在售房总量：',res_block)
    print('---------------->>>>>')
    print('各大区在售房每平米价格均值：',res_block_pre)
    print('---------------->>>>>')
    print('各大区在售房每平米价格中值',res_price_median)
    print('---------------->>>>>')   
    print('各大区在售总面积:',res_size_sum)
 
if __name__ == "__main__":
    main()
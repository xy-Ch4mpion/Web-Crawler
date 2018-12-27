# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from lxml import etree
import re
import random
#from bs4 import BeautifulSoup
import requests
import pandas as pd

result =pd.DataFrame(columns=('商品ID','商品品牌','商品名称','商品毛重','评论数','好评率','价格'))

def id():
    global m_id, result_html
    m_id = []
#    page_id = 2*page - 1
#    url_id = 'https://search.jd.com/search?keyword=%E7%8C%AA%E8%82%89&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=zhurou&ev=3312_34687%5E5397_86385%5E&stock=1&page=' + str(page_id) +'&s=110&click=0'
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(2)
    html = etree.HTML(driver.page_source)
    result_html = etree.tostring(html, encoding = "utf-8", pretty_print= True, method = "html")
    result_html = result_html.decode('utf-8')
    r_id = r'<strong class="J_(.*?)" data-done="1"><em>￥</em>'
    m_id = re.findall(r_id, result_html)
    print(m_id)
#    result_id = requests.get(url_id).text
#    r_id = r'<li data-sku="(.*?)" class'
#    m_m_id = re.findall(r_id, result_id)
#    m_id.append(m_m_id)
#    print(m_m_id)

def items():
    global item_list
    item_list = []
    for id in m_id:
        url = 'https://item.jd.com/%s.html'%(id)
        result_items = requests.get(url).text
        r_items = r"<li title='(.*?)'>商品名称"
        m_items = re.findall(r_items, result_items)
        if m_items:
            item_list.append(m_items[0])
        else:
            item_list.append('NA')
    print(item_list)
    
def weight():
    global weight_list
    weight_list = []
    for id in m_id:
        url = 'https://item.jd.com/%s.html'%(id)
        result_weight = requests.get(url).text
        r_weight = r"<li title='(.*?)'>商品毛重"
        m_weight = re.findall(r_weight, result_weight)
        if m_weight:
            weight_list.append(m_weight[0])
        else:
            weight_list.append('NA')
    print(weight_list)

def brands():
    global brands_brands
    brands_brands = []
    for id in m_id:
        url = 'https://item.jd.com/%s.html'%(id)
        result_brands = requests.get(url).text
        r_brands = r"<li title='(.*?)'>品牌"
        m_brands = re.findall(r_brands, result_brands)
        if m_brands:
            brands_brands.append(m_brands[0])
        else:
            brands_brands.append('NA')
    print(brands_brands)

#def brands():
#    global m_brands
#    m_brands = []
#    for id in m_id:
#        js = 'window.open("https://item.jd.com/%s.html");'%(id)
#        driver.execute_script(js)
#        js = "var q=document.documentElement.scrollTop=100000"
#        driver.execute_script(js)
#        time.sleep(2)
#        html = etree.HTML(driver.page_source)
#        result_html = etree.tostring(html, encoding = "utf-8", pretty_print= True, method = "html")
#        result_html = result_html.decode('utf-8')
#        handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
#        driver.switch_to.window(handles[1])
#        driver.close()
#        handles = driver.window_handles
#        driver.switch_to.window(handles[0])
#        r_brands = r'<li title="(.*?)">'
#        m_brands = re.findall(r_brands, result_html)
#        if m_brands:
#            m_brands.append(m_brands[0])
#        else:
#            m_brands.append('NA')
#    print(m_brands)  
    
def rating():
    global rating_list, rating_countStr
    rating_list = []
    rating_countStr = []
    for id in m_id:
        url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5292&productId='\
            +id+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        result_rating = requests.get(url).text
        r_rating = r'"goodRateShow":(.*?),"poorRateShow'
        r_ratingplus = r'"commentCount":(.*?),"'
        m_rating = re.findall(r_rating, result_rating)
        m_ratingplus = re.findall(r_ratingplus, result_rating)
        for i in range(1,20):
            if m_rating and m_ratingplus:
                rating_list.append(m_rating[0])
                rating_countStr.append(m_ratingplus[0])
                break
            else:
                result_rating = requests.get(url).text
                r_rating = r'"goodRateShow":(.*?),"poorRateShow'
                r_ratingplus = r'"commentCount":(.*?),"'
                m_rating = re.findall(r_rating, result_rating)
                m_ratingplus = re.findall(r_ratingplus, result_rating)
    print(rating_list)
    print(rating_countStr)


def price():
    global m_price
    r_price = r'<em>￥</em><i>(.*?)</i></strong>'
    m_price = re.findall(r_price, result_html)
    print(m_price)
    
def standardize(para):
    if len(para) < 60:
        for i in range(len(para), 60):
            para.append('NA')

if __name__=="__main__":
    loginurl = 'https://search.jd.com/Search?keyword=%E7%8C%AA%E8%82%89&enc=utf-8&wq=%E7%8C%AA%E8%82%89'
    # 打开浏览器
    path = "C:\\Users\\Ehthan\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=path)
    driver.maximize_window()
    driver.get(loginurl)
    assert "猪肉 - 商品搜索 - 京东" in driver.title
    driver.find_element_by_link_text('中国大陆').click()
    driver.find_element_by_link_text('冷藏').click()
    for page in range(0, 7):
        id()
        brands()
        price()
        rating()
        items()
        weight()
        print('page:', page + 1)
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
        driver.find_element_by_class_name('pn-next').click()
        standardize(m_id)
        standardize(rating_list)
        standardize(rating_countStr)
        standardize(brands_brands)
        standardize(item_list)
        standardize(weight_list)
        standardize(m_price)
        result=result.append(pd.DataFrame({'商品ID':m_id,'商品品牌':brands_brands,'商品名称':item_list,'商品毛重':weight_list,'评论数':rating_countStr,'好评率':rating_list,'价格':m_price}),ignore_index=True)
    result.to_excel(r'C:\\Users\\Ehthan\\Desktop\\京东中国大陆冷藏.xls',sheet_name='Sheet1')        
        
        

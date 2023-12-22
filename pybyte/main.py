import time

from selenium import webdriver
from urllib.parse import urljoin
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

wd = webdriver.Edge()
wait = WebDriverWait(wd, 5)

url = 'https://www.pcbyte.com.my/c/pc-components-parts-computer-components-8386'

wd.get(url)
data_list = []
while True:
    # 爬取所有数据
    # 拿数据

    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="products-grid"]')))

    tree = etree.HTML(wd.page_source)
    div_list = tree.xpath('//div[@class="ict-catalog-item-wrap col-12 col-sm-6 col-md-4 col-lg-4 col-xl-3"]')

    for div in div_list:
        title = div.xpath('./div/form/div/div[2]/h3/a/text()')
        price = div.xpath('./div/form/div/div[2]/div[1]/div[1]/span/span/text()')
        in_stock = div.xpath('./div/form/div/div[2]/div[2]/div[3]/text()')
        image_url = div.xpath('./div/form/div/div[1]/a/img/@src')
        href = div.xpath('./div/form/div/div[1]/a/@href')
        data_list.append(
            {
                'title': title[0],
                'price': price[0],
                'in_stock': in_stock[0],
                'image_url': image_url[0],
                'href': urljoin('https://www.pcbyte.com.my/', href[0])
            }
        )
    # 下一页 
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH,'//ul[@class="pagination bottom-pagination"]//a/span[@class="fa fa-chevron-right"]')))
        next_page_href = wd.find_element(By.XPATH, '//ul[@class="pagination bottom-pagination"]//a/span[@class="fa fa-chevron-right"]')
        next_page_href.click()
        time.sleep(1)
    except:
        break

df = pd.DataFrame(data_list)

df.to_csv('data.csv', index=True)
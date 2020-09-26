import requests
from bs4 import BeautifulSoup
import re
import time
import threading
import xlwt
class jd():
    def __init__(self):
        self.Product_Config_list = []
        self.get_ever()

    def get_ever(self):
        self.search='开发板'
        for page in range(-1,2):
            self.url=f'https://search.jd.com/Search?keyword={self.search}&enc=utf-8&wq={self.search}&page={str(page+2)}'
            r=requests.get(url=self.url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'},)
            soup=BeautifulSoup(r.text)
            ul=soup.find('ul',{'class':'gl-warp'})
            url_id=[]
            for li in ul.contents:
                try:
                    url_id.append(li.attrs['data-sku'])
                except:
                    continue
            for id in url_id:
                # threading.Thread(target=,args=[]).start()
                self.get_info(f'https://item.jd.com/{id}.html')
            # self.get_comment()
        while (threading.active_count() != 1):
            time.sleep(1)
        self.Create_Excel()
    def Create_Excel(self):
        pass
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建表,第二参数用于确认同一个cell单元是否可以重设值
        worksheet = workbook.add_sheet(self.search, cell_overwrite_ok=True)

        for i, config in enumerate(self.Product_Config_list[0]):
            worksheet.write(0, i, config.split('：')[0])
        for num,product_conf in enumerate(self.Product_Config_list):
            for i,config in enumerate(product_conf):
                worksheet.write(num+1, i  ,config.split('：')[1])

        workbook.save(f'{self.search}.xls')

    def get_comment(self):
        product_id =re.search('\d{1,}',self.product_url).group(0)

        r = requests.get(url='https://sclub.jd.com/comment/productPageComments.action',
                         headers={'Referer': f'https://item.jd.com/{product_id}.html',
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'},
                         #评论区有很多页。在page可以调
                         params={'callback': 'fetchJSON_comment98vv3625',
                                 'productId': product_id,
                                 'score': '1',
                                 'sortType': '5',
                                 'page': '0',
                                 'pageSize': '10',
                                 'isShadowSku': '0',
                                 'fold': '1'}
             )
        #考虑到只有一个( 和 ) 那就用正则匹配这里面所有的
        comment_dict=re.search("\(.{1,}\)",r.text).group(0)[1:-1].replace('null',"'null'").replace('true',"'true'").replace('false',"'false'")
        comment_dict=eval(comment_dict)
        CommentSummary=comment_dict['productCommentSummary']
        for key,value in CommentSummary.items():
            print(key,value)
        #现在获得统计
        CommentStatistics_list=comment_dict['hotCommentTagStatistics']
        for d in CommentStatistics_list:
            print(f"觉得{d['name']}的有{d['count']}人")
        #现在获得所有的
        Comments=comment_dict['comments']
        for Com in Comments:
            print(Com['content'])
    def get_info(self,url):
        self.product_url=url
        print(self.product_url, '开始')
        product_info=requests.get(url=self.product_url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})
        self.info_soup=BeautifulSoup(product_info.text)
        #商品名字
        sku_name=self.info_soup.find('div',{'class':'sku-name'})
        try:
            self.product_name = sku_name.contents[2]
        except:
            self.product_name=sku_name.contents[0]
        #获得商品类型
        # product_color=self.info_soup.find('div',{'id':'choose-attr-1'})
        # for ever in product_color.contents[3].contents:
        #     if ever == '\n':
        #         continue
        #     else:
        #         print(ever.attrs['data-value'])
        # #获得商品版本
        # product_version=self.info_soup.find('div',{'id':'choose-attr-2'})
        # if product_version:
        #     for ever in product_version.contents[3].contents:
        #         if ever == '\n':
        #             continue
        #         else:
        #             print(ever.attrs['data-value'])
        # else:
        #     print('这个商品没有version..')
        #获得商品参数
        Product_Config=self.info_soup.find('ul',{'class':'parameter2'})
        temp=[]
        for li in Product_Config.contents:
            if li is not 'li' and li.string!='\n' and li.string!=None:
                # print(li.string,end='')
                temp.append(li.string)
        self.Product_Config_list.append(temp)
        # print(self.Product_Config_list)
jd()

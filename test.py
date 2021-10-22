import numpy as np  
from requests.api import request
import requests


thucphamtuoisong_url_page = "https://tiki.vn/api/personalish/v1/blocks/listings"
def crawl_product_id(page, limit, category):
    product_list = np.array([])
    i = 1
    while(i < page):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*"
        }
        params = {
            'page': page,
            'limit': limit,
            'trackity_id': 'b9621f1c-2eeb-595c-bb35-1fb3c89c6a89',
            'category': category
        }
        response = requests.request(
            "GET", thucphamtuoisong_url_page, headers=headers, params=params)
        # print(response)
    #     print("page", i)
    #     y = response.json()
    #     print(len(y["data"]))
    #     for j in range(len(y["data"])):  # vong lap tang y data
    #         idproduct = y["data"][j]['id']
    #         # print("idproduct",idproduct)
    #         product_list = np.append(product_list, idproduct, axis=0)
    #     i += 1
    # product_list = product_list.astype(int)
    # print('product_list', product_list)
    # print('len(product_list)', len(product_list))

product_list = crawl_product_id(1, 48, 44792)





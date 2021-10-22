from bs4 import BeautifulSoup 
import requests  # đọc dữ liệu về
import json  # chuyển thành json để truy cập vào lấy dữ liệu
import csv  # chuyển data thành dạng CSV 
import numpy as np  
import pandas as pd  # đọc và ghi file nhanh hơn
from requests.api import request
from requests.models import Response

list_product_url = "https://tiki.vn/api/personalish/v1/blocks/listings"

detail_product_url = "https://tiki.vn/api/v2/products/{}"

product_rating_url = "https://tiki.vn/api/v2/reviews?limit=5&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page=1&product_id={}"

product_id_file = "./data/product-id.txt"
product_file = "./data/product.txt"
product_file2 = "./data/product-detail.txt"
rating_file = "./data/rating.csv"


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
            'trackity_id': '420f8332-33f6-5506-4287-f288bbcb30d2',
            'category': category
        }
        response = requests.request(
            "GET", list_product_url, headers=headers, params=params)
        print(response)
        print("page", i)
        y = response.json()
        print(len(y["data"]))
        for j in range(len(y["data"])):  # vong lap tang y data
            idproduct = y["data"][j]['id']
            # print("idproduct",idproduct)
            product_list = np.append(product_list, idproduct)
        i += 1
    product_list = product_list.astype(int)
    # print('product_list', product_list)
    # print('len(product_list)', len(product_list))
    return product_list

def write_csv_file(data_matrix, file_path, mode='w'):
    df = pd.DataFrame(data=data_matrix) 
    df.to_csv(file_path, sep=',', encoding='utf-8-sig',
              header=None, index=None, mode=mode)


def read_matrix_file(file_path):
    f = pd.read_csv(
        file_path, sep='\t', encoding='utf-8-sig', header=None)
    f = f.to_numpy()
    return f

def crawl_product(product_list):
    product_detail_list = np.array(
        [['id', 'ten', 'gia', 'phanloai', 'thuonghieu', 'xuatxu', 'xuatxuthuonghieu', 'mota']])
    print('product_detail_list', product_detail_list)
    for product_id in product_list:
        id = -1
        ten = -1
        gia = -1
        phanloai = -1
        thuonghieu = -1
        xuatxu = -1
        xuatxuthuonghieu = -1
        mota = -1
        print("product_id", product_id)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*"
        }

        Response = requests.get(detail_product_url.format(product_id), headers=headers)
        y = Response.json()

        if (Response.status_code == 200):
            id = y['id']
            ten = y['name']
            gia = y['price']
            phanloai = y['productset_group_name']
            thuonghieu = y['brand']['name']
            for i in range(len(y['specifications'][0]['attributes'])):
                if (y['specifications'][0]['attributes'][i]['name'] == "Xuất xứ"):
                    xuatxu = y['specifications'][0]['attributes'][i]['value']
                if (y['specifications'][0]['attributes'][i]['name'] == "Xuất xứ thương hiệu"):
                    xuatxuthuonghieu = y['specifications'][0]['attributes'][i]['value']
            mota = BeautifulSoup(y['description'], 'html.parser').get_text()
        product_detail_list = np.append(
            product_detail_list, [[id, ten, gia, phanloai, thuonghieu, xuatxu, xuatxuthuonghieu, mota]], axis=0)
    return product_detail_list  # luu vao product_detail_list

def crawl_rating(product_list):
    for product_id in product_list:
        userid = -1
        itemid = -1
        rating = -1
        comment = -1
        i = 1
        print("product_id", product_id)
        payload = {}
        params = {"page": i}
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }
        Response = requests.get(product_rating_url.format(
            product_id), headers=headers, data=payload, params=params)
        print("response", Response)
        y = Response.json()
        total_page = y["paging"]["last_page"]
        if (y["paging"]["total"] > 0):
            while (i <= total_page):
                payload = {}
                params = {"page": i}
                headers = {
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
                }
                res = requests.get(product_rating_url.format(
                    product_id), headers=headers, data=payload, params=params)
                x = res.json()
                
                for j in range(len(x["data"])):
                    userid = x["data"][j]['customer_id']
                    itemid = product_id
                    rating = x["data"][j]['rating']
                    comment = x["data"][j]['content']
                    rating_list = np.array([[userid, itemid, rating, comment]])
                    # rating_list = np.array(
                    #     [[userid, itemid, rating, comment]])
                    write_csv_file(rating_list, rating_file, mode='a')
                i += 1  
                
                # df = pd.DataFrame(data=rating_list)
                # df.to_csv(rating_list,rating_file,encoding='utf-8-sig',
                #     header=["User ID","Product_ID","Rate","Timestamp","Comment"], index=None, mode='a')
                    
    return 1

# crawl id tat ca san pham
# product_list = crawl_product_id(2, 48, 44792)

# ghi file cac id san pham vua crawl vao file product-id.txt
# w la ghi de len file co san
# write_csv_file(product_list, product_id_file, mode='w')

# doc danh sach id san pham de tien hanh crawl chi tiet san pham va rating
product_list = read_matrix_file(product_id_file).flatten()

# crawl chi tiet san pham va ghi vao file product.csv
# product_detail_list = crawl_product(product_list)
# write_csv_file(product_detail_list, product_file2, mode='w')

# crawl tat ca rating trong product_list va ghi vao file rating.csv
rating_list = crawl_rating(product_list)

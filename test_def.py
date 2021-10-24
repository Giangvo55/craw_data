import requests  # đọc dữ liệu về
import json  # chuyển thành json để truy cập vào lấy dữ liệu
import csv  # chuyển data thành dạng CSV 
import numpy as np  
import pandas as pd  # đọc và ghi file nhanh hơn
from requests.api import request
from requests.models import Response


detail_product_url = "https://tiki.vn/api/v2/products/{}"

product_rating_url = "https://tiki.vn/api/v2/reviews?limit=5&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page=1&product_id={}"

product_id_file = "./data/product-id.txt"
product_detail = "./data/product-detail.csv"
rating_file = "./data/rating.csv"

def crawl_product(product_list):
    product_detail_list = np.array(
        [['Product_ID', 'Product_Name', 'Product_Price', 'Category', 'Brand', 'Origin', 'Brand_Origin']])
    # print('product_detail_list', product_detail_list)
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*"
        }
    for product_id in product_list:
        id = -1
        ten = -1
        gia = -1
        phanloai = -1
        thuonghieu = -1
        xuatxu = -1
        xuatxuthuonghieu = -1
        # mota = -1
        print("product_id", product_id)

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
            # mota = BeautifulSoup(y['description'], 'html.parser').get_text()
                product_detail_list = np.append(
                        product_detail_list, [[id, ten, gia, phanloai, thuonghieu, xuatxu, xuatxuthuonghieu]], axis=0)
    return product_detail_list  # luu vao product_detail_list


def read_matrix_file(file_path):
    f = pd.read_csv(
        file_path, sep='\t', encoding='utf-8-sig', header=None)
    f = f.to_numpy()
    return f

def write_csv_file(data_matrix, file_path, mode='w'):
    df = pd.DataFrame(data=data_matrix) 
    df.to_csv(file_path, sep=',', encoding='utf-8-sig',
              header=None, index=None, mode=mode)

def crawl_rating(product_list):
    rating_list = np.array([["User_id", "Item_id", "Rating", "Comment"]])
    headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }
    for product_id in product_list:
        userid = -1
        itemid = -1
        rating = -1
        comment = -1
        i = 1
        print("product_id", product_id)
        payload = {}
        params = {"page": i}

        Response = requests.get(product_rating_url.format(
            product_id), headers=headers, data=payload, params=params)
        print("response", Response)
        y = Response.json()
        total_page = y["paging"]["last_page"]
        if (y["paging"]["total"] > 0):
            while (i <= total_page):
                payload = {}
                params = {"page": i}
                # headers = {
                #     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
                # }
                res = requests.get(product_rating_url.format(
                    product_id), headers=headers, data=payload, params=params)
                x = res.json()
                
                for j in range(len(x["data"])):
                    userid = x["data"][j]['customer_id']
                    itemid = product_id
                    rating = x["data"][j]['rating']
                    comment = x["data"][j]['content']
                    rating_list = np.append(
                        rating_list, [[userid,itemid,rating,comment]], axis=0
                    )
                    # rating_list = np.array([[userid, itemid, rating, comment]])
                    # rating_list = np.array(
                    #     [[userid, itemid, rating, comment]])
                    # write_csv_file(rating_list, rating_file, mode='a')
                i += 1           
    return rating_list

product_list = read_matrix_file(product_id_file).flatten()
# write_csv_file(product_detail_list, product_file2, mode='w')
# product_detail_list = crawl_product(product_list)
# write_csv_file(product_detail_list,product_detail, mode="w")
# crawl tat ca rating trong product_list va ghi vao file rating.csv
rating_list = crawl_rating(product_list)
write_csv_file(rating_list, rating_file, mode="w")
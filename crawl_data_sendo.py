import csv
import json

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.models import parse_header_links

list_product_url = "https://searchlist-api.sendo.vn/web/categories/2403/products"

detail_product_url = "https://detail-api.sendo.vn/full/{}?source_block_id=listing_products"

rating_url = "https://ratingapi.sendo.vn/product/{}/rating"

product_id_file = "./data/product-id.txt"
product_file = "./data/product-detail.csv"
rating_file = "./data/rating.csv" 
category_path_file ="./data/product-category-path.txt"

def crawl_product_id(page,size):
    product_list = np.array([])
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "origin":"https://www.sendo.vn",
            "referer":"https://www.sendo.vn/"
        }

    i = 1
    while(i < page):
        payload = {}
        params = {
           'listing_algo':'algo13',
           'page': i,
           'platform':'web',
           'size': size,
           'sortType': 'listing_v2_desc'

        }
        response = requests.request("GET", list_product_url, headers=headers, params=params, data= payload)
        # print(response)
        print("page", i)
        y = response.json()
        print(len(y["data"]))
        for j in range(len(y["data"])):  # vong lap tang y data
            idproduct = y["data"][j]['id']
            print("idproduct",idproduct)
            product_list = np.append(product_list, idproduct)
        i += 1
    product_list = product_list.astype(int)
    # print('product_list', product_list)
    print('Total Product ID: ', len(product_list))
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

def crawl_category_path(page,size):
    category_path = np.array([])
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "origin":"https://www.sendo.vn",
            "referer":"https://www.sendo.vn/"
        }

    i = 1
    while(i < page):
        payload = {}
        params = {
           'listing_algo':'algo13',
           'page': i,
           'platform':'web',
           'size': size,
           'sortType': 'listing_v2_desc'

        }
        response = requests.request("GET", list_product_url, headers=headers, params=params, data= payload)
        # print(response)
        print("page", i)
        y = response.json()
        print(len(y["data"]))
        for j in range(len(y["data"])):  # vong lap tang y data
            path = y["data"][j]['category_path']
            category_path = np.append(category_path, path)
        i += 1
    # product_list = product_list.astype(int)
    # print('product_list', product_list)
    print('Total path: ', len(category_path))
    return category_path

def crawl_product(category_list):
    product_detail_list = np.array(
        [['Product_ID', 'Product_Name', 'Product_Price', 'Category', 'Brand', 'Origin','Total rated']])
    # print('product_detail_list', product_detail_list)
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*"
        }
    
    for path in category_list:
        id = -1
        ten = -1
        gia = -1
        phanloai = -1
        thuonghieu = -1
        xuatxu = -1
        tongsodanhgia = 0 
        
        x = path.replace(".html", "") 
        Response = requests.get(detail_product_url.format(x),headers=headers)
        y = Response.json()

        if (Response.status_code == 200):
            id = y['data']['id']
            ten = y['data']['name']
            gia = y['data']['price']
            phanloai = y['data']['category_info'][2]['title']
            thuonghieu = y['data']['shop_info']['shop_name']
            xuatxu = y['data']['shop_info']['warehourse_region_name']
            tongsodanhgia = y['data']['rating_info']['total_rated']
            product_detail_list = np.append(
                        product_detail_list, [[id, ten, gia, phanloai, thuonghieu, xuatxu, tongsodanhgia]], axis=0)
            print("Sucessful! ")
    return product_detail_list  # luu vao product_detail_list

def crawl_rating(product_file):
    headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }

    rating_list = np.array([["User_id", "Item_id", "Rating", "Comment"]])
    
    df = pd.read_csv(product_file)

    for i in range(len(df)):
        userid = -1
        itemid = df.iloc[i]['Product_ID']
        star = -1
        comment = -1 
        
        if(df.iloc[i]['Total rated']==0):
            continue
        else:
            params = {
                'limit' : df.iloc[i]['Total rated'],  
                'sort' : 'review_score', 
                'v' : 2, 
                'star': all
            }
            Response = requests.get(
                rating_url.format(df.iloc[i]['Product_ID']), headers=headers, params=params)
            print(Response.status_code)
            x = Response.json()
            for j in range(len(x["data"])):
                userid = x["data"][j]["customer_id"]
                star = x["data"][j]["star"]
                comment = x["data"][j]["comment"]
                rating_list = np.append(
                    rating_list, [[userid,itemid,star,comment]], axis =0
                )

    return rating_list
                

#Lưu ID sản phẩm
# product_list = crawl_product_id(50,60)
# write_csv_file(product_list, product_id_file, mode='w')
# product_list = read_matrix_file(product_id_file).flatten()

#Lưu đường dẫn của từng product 
# category_path = crawl_category_path(50,60)
# write_csv_file(category_path, category_path_file, mode='w')

#Cào dữ liệu sản phẩm :
# category_list = read_matrix_file(category_path_file).flatten()
# product_detail_list = crawl_product(category_list)
# write_csv_file(product_detail_list, product_file, mode='w')

#Cào rating sản phẩm
# rating_list = crawl_rating(product_file)
# write_csv_file(rating_list, rating_file, mode ="w")






#-*- coding: utf-8 -*-
import requests
import winsound
# import datetime
from datetime import datetime
import random
import pandas as pd
import numpy as np
import csv
import time
import os
import re
# pip install pymysql
import pymysql

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# pip install selenium
from bs4 import BeautifulSoup
from os.path import join
from collections import defaultdict
from collections import Counter
from statistics import mean
from pandas_datareader import data as pder
from io import StringIO



def craw_page():
	# 增加瀏覽紀錄
	url_arr = ["https://www.google.com.tw/search?q=rehacare&sca_esv=571399955&hl=zh_TW&source=hp&ei=mbwgZZrLJvrM2roPiKizyAI&iflsig=AO6bgOgAAAAAZSDKqR6oc7JXvsWdoMR2EyF0zFnsnVON&ved=0ahUKEwja-7yu7OKBAxV6plYBHQjUDCkQ4dUDCAw&uact=5&oq=rehacare&gs_lp=Egdnd3Mtd2l6IghyZWhhY2FyZTIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIzA5QggJYhQxwAXgAkAEAmAFLoAHNAqoBATW4AQPIAQD4AQL4AQGoAgDCAgQQABgewgIGEAAYCBgewgIGEAAYHhgK&sclient=gws-wiz", "https://www.rehacare.com/", "https://www.rehacare.com/en/companies-products/exhibitors-list", "https://www.rehacare.com/vis/v1/en/search?ticket=g_u_e_s_t&_query=&f_type=profile"]
	url1 = "https://www.google.com.tw/?hl=zh_TW"
	url2 = "https://www.google.com.tw/search?q=rehacare&sca_esv=571399955&hl=zh_TW&source=hp&ei=mbwgZZrLJvrM2roPiKizyAI&iflsig=AO6bgOgAAAAAZSDKqR6oc7JXvsWdoMR2EyF0zFnsnVON&ved=0ahUKEwja-7yu7OKBAxV6plYBHQjUDCkQ4dUDCAw&uact=5&oq=rehacare&gs_lp=Egdnd3Mtd2l6IghyZWhhY2FyZTIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIzA5QggJYhQxwAXgAkAEAmAFLoAHNAqoBATW4AQPIAQD4AQL4AQGoAgDCAgQQABgewgIGEAAYCBgewgIGEAAYHhgK&sclient=gws-wiz"
	url3 = "https://www..../"
	url4 = "https://www...."
	url5 = "https://www...."

	# 創建ChromeOptions
	chrome_options = Options()

	# 設置ChromeOptions背景執行
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-gpu")

	driver = webdriver.Chrome(options=chrome_options)

	driver.get(url1)
	for url_i in url_arr:
		# driver = webdriver.Chrome()
		driver.get(url_i)
		print("到站:" + str(url_i))
		time.sleep(random.uniform(3.2, 4.4))

	# 必須要確認是否已經拉到底
	for ctn in range(1, 2):
		# 卷軸往下拉
		print("下拉次數: " +str(ctn))
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# 模擬使用者
		time.sleep(random.uniform(3.2, 6.4))

	# 抓到目前所有的資料 先寫入txt (備用)
	# print(driver.page_source)
	page_source_string = driver.page_source

	with open("com_list_page_source_string.txt", "w", encoding='utf-8') as file:
		file.write(page_source_string)

	time.sleep(random.uniform(10.8, 18.24))
	driver.quit()

	comp_data = [];
	error_data = [];
	soup = BeautifulSoup(page_source_string, 'html.parser')

	com_llist_num = len(soup.find_all(class_='media-module__link', attrs={"data-pos": True}))
	process_no = 1

	# 抓取每一筆公司名稱+簡介網址
	for i in soup.find_all(class_='media-module__link', attrs={"data-pos": True}):
		try:
			comp_sub_list = []
			comp_sub_list.append(i.find("h3").text.replace("\n", ""))
			comp_sub_list.append(("https://www.rehacare.com/" + i['href']).replace("\n", ""))

			# if "Angel Robotics CO.,LTD" in i.find("h3").text:
			print("當前進度: ", str(process_no)+'/'+str(com_llist_num) , datetime.now(), '_____',i.find("h3").text, " : ", "https://www.rehacare.com/" + i['href'])

			# 背景執行
			chrome_options2 = Options()
			chrome_options2.add_argument("--headless")
			chrome_options2.add_argument("--disable-gpu")

			driver2 = webdriver.Chrome(options=chrome_options2)
			driver2.get("https://www.google.com.tw/?hl=zh_TW")
			time.sleep(random.uniform(2.4, 5.8)) # 模擬正常操作
			driver2.get("https://www.rehacare.com/")
			time.sleep(random.uniform(2.4, 5.8))
			driver2.get("https://www.rehacare.com/" + i['href'])
			time.sleep(random.uniform(5.4, 9.8))

			elementx = driver2.find_element(By.XPATH, '//*[@id="finder-profile"]/div/div/section/div/div/div[2]/div[5]/button/div/span')
			elementx.click()
			# print(driver2.page_source)

			# 獲取公司資料
			soup2 = BeautifulSoup(driver2.page_source, 'html.parser')
			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="address-street").text)
			except Exception as e0:
				comp_sub_list.append("")

			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="address-zip").text)
			except Exception as e1:
				comp_sub_list.append("")

			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="address-city").text)
			except Exception as e2:
				comp_sub_list.append("")

			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="address-country").text)
			except Exception as e3:
				comp_sub_list.append("")

			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="exh-contact-email").text.replace("E-mail: ", ""))
			except Exception as e4:
				comp_sub_list.append("")

			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="exh-contact-phone").text.replace("Phone: ", ""))
			except Exception as e5:
				comp_sub_list.append("")

			try:
				comp_sub_list.append(soup2.find(id="profile-business-data").find(class_="exh-contact-links").text.replace("Web:", ""))
			except Exception as e6:
				comp_sub_list.append("")

			c_time = datetime.now()
			now_datetime0 = c_time.strftime("%Y-%m-%d %H:%M:%S")
			comp_sub_list.append('0')
			comp_sub_list.append(now_datetime0)
			comp_sub_list.append(now_datetime0)

			# print(comp_sub_list)
			comp_data.append(comp_sub_list)

			dbarr = []
			dbarr.append(comp_sub_list)
			insert_into_table(dbarr, '0')
			# 寫入資料庫		

		except Exception as e:
			print("錯誤資料:" + e)
			try:
				error_data.append(i.find("h3").text, " : ", "https://www.rehacare.com/" + i['href'])
			except Exception as e:
				print("錯誤訊息")
				print(e)
			
		process_no += 1

		time.sleep(random.uniform(5.24, 12.24))
		driver2.quit()

	# 寫入excel
	df = pd.DataFrame(comp_data)
	df_error = pd.DataFrame(error_data)

	# 保存到Excel文件
	df.to_excel('company_data.xlsx', index=False)
	df_error.to_excel('error_data.xlsx', index=False)
		

def readAndParse():
	ftxt = open('output.txt', 'r', encoding='utf-8')
	contain = ftxt.read()
	# print(contain)
	soup = BeautifulSoup(contain, 'html.parser')
	# print(soup.find_all(class_='media-module__link'))

	com_list = []
	for i in soup.find_all(class_='media-module__link', attrs={"data-pos": True}):
		print("https://www.rehacare.com/" + i['href'], ',', i.find("h3").text)
		com_list.append([i.find("h3").text, "https://www.rehacare.com/" + i['href']])

	df = pd.DataFrame(com_list)

	# 保存到Excel文件
	df.to_excel('company_data.xlsx', index=False)


def check_com_list():
	# db connect
	cnx = pymysql.connect(
	    host="localhost",
	    user="root",
	    password="1043309",
	    database="test"
	)
	cursor = cnx.cursor()


	ftxt_ = open('com_list_page_source_string.txt', 'r', encoding='utf-8')
	contain_1 = ftxt_.read()

	soup = BeautifulSoup(contain_1, 'html.parser')

	print('資料筆數: ', len(soup.find_all(class_='media-module__link', attrs={"data-pos": True})))

	cl_cter = 1
	for i in soup.find_all(class_='media-module__link', attrs={"data-pos": True}):
		print(cl_cter, "https://www.rehacare.com/" + i['href'], ',', i.find("h3").text)

		# 寫入的sql
		sql = "INSERT INTO crawler (company_name, intro_url) VALUES (%s, %s)"
		values = (i.find("h3").text.replace("\n", ""), 'https://www.rehacare.com/' + i['href'])

		# 執行並提交
		# cursor.execute(sql, values)
		# cnx.commit()
		# time.sleep(1)

		cl_cter += 1
	# 關閉
	cursor.close()
	cnx.close()

def excel_to_db():
	# excel 轉入 db
	cnx = pymysql.connect(
		host="localhost",
		user="root",
		password="1043309",
		database="project_c"
	)

	df = pd.read_excel('company_data.xlsx')
	df = df.replace({np.nan: None})
	current_time = datetime.now()
	now_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")


	cursor = cnx.cursor()
	current_time = datetime.now()

	now_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")
	# print(len(df), now_datetime)

	format_arr_dates = []
	for df_i in range(len(df)):
		print(df_i, df.iloc[df_i, :][0].replace("                            ", ""), df.iloc[df_i, :][1], df.iloc[df_i, :][2], df.iloc[df_i, :][3], df.iloc[df_i, :][4], df.iloc[df_i, :][5], df.iloc[df_i, :][6], df.iloc[df_i, :][7], df.iloc[df_i, :][8], now_datetime)
		format_arr_dates.append([
			df.iloc[df_i, :][0].replace("                            ", "") ,
			df.iloc[df_i, :][1], 
			df.iloc[df_i, :][2], 
			df.iloc[df_i, :][3], 
			df.iloc[df_i, :][4], 
			df.iloc[df_i, :][5], 
			df.iloc[df_i, :][6], 
			df.iloc[df_i, :][7], 
			df.iloc[df_i, :][8],
			])

		sql = "INSERT INTO crawler (company_name, intro_url , street, zip, city, country, email , phone, links, craw_status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (
			df.iloc[df_i, :][0].replace("                            ", "") ,
			df.iloc[df_i, :][1], 
			df.iloc[df_i, :][2], 
			df.iloc[df_i, :][3], 
			df.iloc[df_i, :][4], 
			df.iloc[df_i, :][5], 
			df.iloc[df_i, :][6], 
			df.iloc[df_i, :][7], 
			df.iloc[df_i, :][8],
			'0',
			now_datetime,
			now_datetime)

		# 執行並提交
		cursor.execute(sql, values)
		cnx.commit()
		time.sleep(1)

	sql2 ="UPDATE `crawler` SET `craw_status`='1' WHERE `craw_status`='0'"

	# 執行並提交
	cursor.execute(sql2)
	cnx.commit()

	cursor.close()
	cnx.close()

	# insert_into_table(format_arr_dates, '0')


def insert_into_table(rst_datas, is_truncate):
	# rst_data = [1,1,1,1,1,,1,1]; is_truncate是否需要先清空資料表

	cnx = pymysql.connect(
	    host="localhost",
	    user="root",
	    password="paswd123456",
	    database="project_c"
	)
	cursor = cnx.cursor()

	if is_truncate == '1':
		print('--- TRUNCATE TABLE ---')
		table_name = 'crawler'
		sql = f"TRUNCATE TABLE {table_name}"
		cursor.execute(sql)
		cnx.commit()

	current_time = datetime.now()
	now_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")

	for rst_data in rst_datas:
		print(rst_data)

		sql = "INSERT INTO crawler (company_name, intro_url , street, zip, city, country, email , phone, links, craw_status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (
			rst_data[0], 
			rst_data[1], 
			rst_data[2], 
			rst_data[3], 
			rst_data[4], 
			rst_data[5], 
			rst_data[6], 
			rst_data[7], 
			rst_data[8],
			'0',
			now_datetime,
			now_datetime)

		# 執行並提交
		cursor.execute(sql, values)
		cnx.commit()
		time.sleep(2)

	cursor.close()
	cnx.close()

def update_status_1():

	cnx = pymysql.connect(
	    host="localhost",
	    user="root",
	    password="paswd123456",
	    database="project_c"
	)
	cursor = cnx.cursor()

	sql2 ="UPDATE `crawler` SET `craw_status`='1' WHERE `craw_status`='0'"

	# 執行並提交
	cursor.execute(sql2)
	cnx.commit()
	time.sleep(1)

	cursor.close()
	cnx.close()

def xls_insert_into():
	df = pd.read_excel('company_data.xlsx')
	df = df.replace({np.nan: None})

	current_time = datetime.now()
	now_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")

	cnx = pymysql.connect(
	    host="localhost",
	    user="root",
	    password="paswd123456",
	    database="project_c"
	)
	cursor = cnx.cursor()

	for df_i in range(len(df)):

		sql = "INSERT INTO crawler (company_name, intro_url , street, zip, city, country, email , phone, links, craw_status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (df.iloc[df_i, :][0].replace("                            ", ""), df.iloc[df_i, :][1], df.iloc[df_i, :][2], df.iloc[df_i, :][3], df.iloc[df_i, :][4], df.iloc[df_i, :][5], df.iloc[df_i, :][6], df.iloc[df_i, :][7], df.iloc[df_i, :][8], '0', now_datetime, now_datetime)

		cursor.execute(sql, values)
		cnx.commit()

		print(values)
		time.sleep(0.5)

	sql2 ="UPDATE `crawler` SET `craw_status`='1' WHERE `craw_status`='0'"

	# 執行並提交
	cursor.execute(sql2)
	cnx.commit()
		
	cursor.close()
	cnx.close()


if __name__=='__main__':
	craw_page()
	


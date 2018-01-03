# !python3
# wineData.py - collects as much data as possible from LCBO's API
'''
***TODO***
-create xlsx with name, price, rating

-import pandas and create dataframe
-make simple graph
'''

import requests
import json
import openpyxl
from wineData_pass import *

# LCBO API 
TOKEN_ACCESS_KEY = GITHUB_TOKEN_ACCESS_KEY
LCBO_URL = 'https://lcboapi.com/products'

# Global wine score API 
TOKEN = GITHUB_TOKEN 
GWS_URL = 'https://api.globalwinescore.com/globalwinescores/latest'

# Global iterator for writing to spreadsheet
row_iter = 2

def lcbo_api():
	# Get json
	payload = {'access_key':TOKEN_ACCESS_KEY,
				'per_page':100,
				'q':'red+wine'
				}
	r = requests.get(LCBO_URL, payload)
	wine_data_init = json.loads(r.text)
		
	# Find total records and pages in 'pager' section of json
	wine_pager = wine_data_init.get('pager') # not a typo
	wine_pages = int(wine_pager.get('total_pages'))
	wine_records = int(wine_pager.get('total_record_count'))

	
	# Create workbook
	wb = openpyxl.Workbook()
	wb.title = 'wineData'
	sheet = wb.active
	
	# Create columns with headers
	sheet['A1'] = 'name'
	sheet['B1'] = 'price'
	
	# TODO: change to (wine_pages + 1)
	for i in range(1, 3):
		
		# Add page element to requests dictionary
		payload['page'] = i
		r_pages = requests.get(LCBO_URL, payload)
		wine_data_final = json.loads(r_pages.text)
		
		# Print progress by page
		print('Reading JSON page %i of %i...' % (i, wine_pages))
		
		# Loop thru each json page	
		for j in range(0, 100): # 1 less than 100 per page (indexing)
			
			# Get desired data from JSON element (record) 
			wine_results = wine_data_final.get('result')
			name = wine_results[j].get('name')
			price = int(wine_results[j].get('price_in_cents'))
			
			# Bring in row_iter
			global row_iter
			
			# Write data to next row
			sheet.cell(row = row_iter, column = 1).value = name
			sheet.cell(row = row_iter, column = 2).value = price	
			
			# Increment row_iter
			row_iter += 1
			
	wb.save('wineData.xlsx')
			
def wine_score_api():
	payload = {}
				
	r = requests.get(GWS_URL, TOKEN)
	print(r.url)

def data_work():
	pass
	
		
	
	
	
lcbo_api()
# wine_score_api()
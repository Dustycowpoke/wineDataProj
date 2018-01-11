# wineData.py - collects as much data as possible from LCBO's API

#***TODO***
# only returning 1 page

import requests
import json
import openpyxl
from wineData_pass import *

# LCBO API 
TOKEN_ACCESS_KEY = GITHUB_TOKEN_ACCESS_KEY
LCBO_URL = 'https://lcboapi.com/products'
results_per_page = 100

# Global wine score API 
GWS_URL = 'https://api.globalwinescore.com/globalwinescores/latest'
TOKEN = GITHUB_TOKEN 

# Global iterator for writing to spreadsheet
row_iter = 2

def lcbo_api():
	
	# Get json
	payload = {'access_key':TOKEN_ACCESS_KEY,
				'per_page': results_per_page,
				'q':'bordeaux',
				'is_dead':'false'
				}
	r = requests.get(LCBO_URL, payload)
	wine_data_init = json.loads(r.text)
		
	# Find total records and pages in 'pager' section of json
	# this data is constant per every API call
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
	
	# Run code for every page
	for i in range(1, (wine_pages + 1)):
		
		# Check if on first page
		first_page_TF = wine_pager.get('is_first_page')
		
		# If true, leave the page number out of the payload
		if first_page_TF == True:
		
			r_pages = requests.get(LCBO_URL, payload)
		
		# Otherwist, add page to payload (page=1 actually second page)
		elif first_page_TF == False:
			
			payload['page'] = i
			
			r_pages = requests.get(LCBO_URL, payload)
		
		
		r_pages = requests.get(LCBO_URL, payload)
		
		wine_data_final = json.loads(r_pages.text)
		
		# Print progress by page
		print('Reading JSON page %i of %i... at %s' % (i, wine_pages, r_pages.url))
		
		# Loop thru each json page
		# Can't assume that there are exactly 100 per page
		wine_results = wine_data_final.get('result')
		current_page_record_count = int(wine_pager.get('current_page_record_count'))
		
		global row_iter
		
		for j in range(0, (current_page_record_count - 1)):
		
			name = wine_results[j].get('name')
			price = int(wine_results[j].get('price_in_cents'))
					
			# Write data to next row
			sheet.cell(row = row_iter, column = 1).value = name
			sheet.cell(row = row_iter, column = 2).value = price
			
			# Increment row_iter
			row_iter += 1
	
	wb.save('wineData.xlsx')
			
def wine_score_api():
	
	headers = {'Authorization': ' Token %s' % TOKEN}
	
	r = requests.get(GWS_URL, headers)
	print(r.url)
	
	#with open ('wine_url.txt', 'w') as textfile:
		#textfile.write(r.url)

def data_work():
	pass
	
	
	
lcbo_api()
# wine_score_api()
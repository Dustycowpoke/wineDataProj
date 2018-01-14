# wineData.py - collects as much data as possible from LCBO's API

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

# Global spreadsheet object
wb = openpyxl.Workbook()
wb.title = 'wineData'
sheet = wb.active
# Create columns with headers
sheet['A1'] = 'name'
sheet['B1'] = 'price'
	
def lcbo_api():
	
	# Send payload to API
	payload = {'access_key':TOKEN_ACCESS_KEY,
				'per_page': results_per_page,
				'q':'bordeaux', #change this depending on GWS API availability
				'is_dead':'false'
				}
	
	# Pass payload to API then to text object
	page_1_obj = requests.get(LCBO_URL, payload)
	page_1_doc = json.loads(page_1_obj.text)
		
	# Find total pages in 'pager' section
	page_1_pager = page_1_doc.get('pager')
	total_pages = page_1_pager.get('total_pages')
	wine_records_on_page = int(page_1_pager.get('current_page_record_count'))
	
	# Get results from page 1
	wine_results = page_1_doc.get('result')
	
	# Go thru records on page 1, notify user
	print('Working on page 1 of %s' % total_pages)
	excel_writer(wine_records_on_page, wine_results)
	
	# Loop thru every subsequent page
	for page in range(2, (total_pages + 1)):
		
		print('Working on page %i of %s' % (page, total_pages))
		payload['page'] = page
		page_obj = requests.get(LCBO_URL, payload)
		page_doc = json.loads(page_obj.text)
		
		# Get results on this page
		page_pager = page_doc.get('pager')
		wine_results = page_doc.get('result')
		
		# Find wine records on page
		wine_records_on_page = int(page_pager.get('current_page_record_count'))
		
		# Go thru records on each page
		excel_writer(wine_records_on_page, wine_results)
	
	print('LCBO data: done')
	
def excel_writer(num_records, results):

	# Bring in total rows written in Excel and sheet object
	global row_iter
	global sheet
	
	for j in range(0, (num_records)):
			
			name = results[j].get('name')
			price = int(results[j].get('price_in_cents'))
						
			# Write data to next row
			sheet.cell(row = row_iter, column = 1).value = name
			sheet.cell(row = row_iter, column = 2).value = price
				
			# Increment row_iter
			row_iter += 1
	
	# Save data just written	
	wb.save('wineData.xlsx')
	return
	
def wine_score_api(row, sheet):
	
	header = {'Authorization': 'Token %s' % TOKEN}
	
	payload = {'wine':'bordeaux'}
	
	r = requests.get(GWS_URL, payload, headers=header)
	r_doc = json.loads(r.text)
	print(json.dumps(r_doc, indent=4))

# test function
def wine_score_api_pass_val(sheet):
	
	header = {'Authorization': 'Token %s' % TOKEN}
	
	for row in sheet.iter_rows(min_row=2, max_col=1, max_row=20): 
		payload = {'wine':row}
		
		r = requests.get(GWS_URL, payload, headers=header)
		r_doc = json.loads(r.text)
		print(json.dumps(r_doc, indent=4))

lcbo_api()
#wine_score_api(row_iter, sheet)

wine_score_api_pass_val(sheet)
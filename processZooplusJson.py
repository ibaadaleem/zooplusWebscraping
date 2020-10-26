import pandas as pd
from

jsonFilePath = 'C:\\Users\\Ibaad\\Documents\\ZooplusWebScraper\\outputFiles\\canned_cat_food_pouches.json'


with open(jsonFilePath, encoding='utf-8') as f:   
	data = json.load(f)    
	
#due to nested strucutre, output into multiple dataframes
#and merge on brand name after


df1 = pd.io.json.json_normalize(data, record_path=['productList'], meta='brandName')
df2 = pd.io.json.json_normalize(data, record_path=['productList','skuList'], meta='brandName')


df3 = df1.merge(df2, 'inner', 'brandName')

#drop unnecessary unnested columns
df3 = df3.drop('skuList', 1)
	
	

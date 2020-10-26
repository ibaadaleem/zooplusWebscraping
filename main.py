import json
import scrapeZooplus


def writeJson(fileContents, outputFilePath):
	with open(outputFilePath,'w', encoding='utf8') as fout:
		json.dump(fileContents,fout,indent=2,sort_keys=True,ensure_ascii=False)	

def main(zooPlusUrl, shopUrl, outputFilePath):	
	brandList = scrapeZooplus.scrapeZooplus(zooPlusUrl, shopUrl)
	writeJson(brandList, outputFilePath)

if __name__ == "__main__":
	zooPlusUrl = 'https://www.zooplus.co.uk' 
	shopUrl = '/shop/cats/dry_cat_food'
	
	foodType = shopUrl[len(shopUrl)-shopUrl[::-1].index('/'):len(shopUrl)]
	outputFilePath = f'C:\\Users\\Ibaad\\Documents\\ZooplusWebScraper\\outputFiles\\{foodType}.json'	

	main(zooPlusUrl, shopUrl, outputFilePath)
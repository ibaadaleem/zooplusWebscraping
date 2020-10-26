from bs4 import BeautifulSoup
import requests


def getZooplusSoup (zooPlusUrl, url):
	try:
		res = requests.get(zooPlusUrl+url)
		res.raise_for_status()
		soup = BeautifulSoup(res.text, 'html5lib')
		#track where the scraping is up to
		print(url)
		
		return soup
		
	except HTTPError:
		print (f'{zooPlusUrl}{url} invalid')
		raise 


def scrapeZooplus(zooPlusUrl, shopUrl):
	try:		
		#find all the urls on the page only dive into them if they are
		#a subset of the current URL
		soup = getZooplusSoup(zooPlusUrl, shopUrl)
		foodBrands = soup.select('a[href]')

		#use a set to eliminate duplicates on the website
		foodBrandUrls = set()
		for foodBrandUrl in foodBrands:
			if (foodBrandUrl.get('href').startswith(shopUrl)) and (foodBrandUrl.get('href') != shopUrl):
				foodBrandUrls.add(foodBrandUrl.get('href'))


		#now go through each url and get all the products
		brandList = []
		for brandUrl in foodBrandUrls:
			#brandName is the last part of the URL
			brandName = brandUrl[len(brandUrl)-brandUrl[::-1].index('/'):len(brandUrl)]
			
			brandSoup = getZooplusSoup(zooPlusUrl, brandUrl)
			products = brandSoup.find_all('div',{'data-zta':'productList'})
			products = set(products)
			
			productList = []
			for product in products:
				productDesc = product.find('p',{'class','product__description__text hidden-xs'}).object.text
				productTitle = product.find('a',{'data-zta':'productListLink'}).get('title')
				productUrl = product.find('a',{'data-zta':'productListLink'}).get('href')
				#ID is the last part of the URL
				productId = productUrl[len(productUrl)-productUrl[::-1].index('/'):len(productUrl)]
				
				#Get all the skus that sit under the product
				productSoup = getZooplusSoup(zooPlusUrl, productUrl)
				skus = productSoup.select('div[data-variant-id]')
				
				skuList = []
				for sku in skus:
					skuName = ''
					skuPrice = ''
					skuCurrency = ''
					skuId = ''
								
					temp = sku.find('div', {'class','product__varianttitle'})
					if temp is not None:
						skuName = temp.contents[0].strip()
					
					temp = sku.find('meta', {'itemprop':'price'})
					if temp is not None:
						skuPrice = temp.get('content')
						
					temp = sku.find('meta', {'itemprop':'priceCurrency'})
					if temp is not None:
						skuCurrency = temp.get('content')
						
					skuId = sku['data-variant-id']
						
					skuDict = {
					'skuName':skuName
					,'skuPrice':skuPrice
					,'skuCurrency':skuCurrency
					,'skuId':skuId
					}

					skuList.append(skuDict)

				productDict = {
				'productTitle':productTitle
				,'productId':productId
				,'productDesc':productDesc
				,'skuList':skuList
				}
				
				productList.append(productDict)
				
			brandDict = {
			'brandName':brandName
			,'productList':productList
			}
				
			brandList.append(brandDict)	
	
		return brandList	
	
	except:
		print('Error when parsing through GetZooplusSoup')
		raise
		
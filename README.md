# **fashion Web Scraping.**
Product data scraping from Ecom website.

### **Introduction** 

Coming off the ages in AI filed we all know how essential having data. For someone working on say a, product data for anygiven product sold online, but you dont have it readily available.What to do, with no data.😲

What if I say there is a work around, where you can actually scrape the data from a Ecom website with few simple steps using Python code.😁

### **Python Package**

[Scrapy](https://scrapy.org/) , as the name says is to scrape data from website. Scrapy spider, would crawl through the website to fetch the data of fields we initialize.

### **Code Walkthrough**

We would be scraping from this ecom website, [BOYNER](https://www.boyner.com.tr). We can scrape for all pages in the website.

Scraped product data consists of Name, Brand, Price, ImageURL, and ProductURL.

**Steps**

1. Create a virtual environment,and install the requirements.txt in the directory you want. 

        $ pip install -r requirements.txt

2. Setup scrapy project to get the necessary files.

        $ scrapy startproject #YourFoldername
        $ cd #YourFoldername

3. Create project folders.

        $ mkdir csvFiles
        $ mkdir images_scraped
        $ mkdir jsonFiles
        $ mkdir utilityScripts

    Project folders and files

    ![Folder structure ](Images_for_blog\Screenshot (114).png )

    **'csvfiles'** folder contains CSV files containing webiste to be scraped. Spiders will be reading from those CSV files to get **'starting URLs'** to initiate scraping.

    **‘fashionWebScraping’** folder contains the Scrapy spiders and helper scripts like **‘settings.py’**, **‘item.py’** and **‘pipelines.py’**. We have to modify some of those Scrapy helper scripts to carry out the scraping process successfully.

4. Populate the CSV files with start URL's for each website.

    ![Folder structure ](Images_for_blog\Screenshot (114).png )

    The URL of first page of website we scrape looks like this. 

        https://www.boyner.com.tr/kadin-canta-c-1005/1/?dropListingPageSize=90

5. Modifing 'item.py' and 'settings.py'.

    We define the Item objects to scrape data in 'items.py'.

        # items.py file in fashionWebScarping folder.

        import scrapy
        from scrapy.item import Item, Field

        class FashionwebscrapingItem(scrapy.Item):
        
            #product related items
            gender=Field()
            productId=Field()
            productName=Field()
            priceOriginal=Field()
            priceSale=Field()

            #items to store links 
            imageLink = Field()
            productLink=Field()

            #item for company name
            company = Field()

            #items for image pipeline
            #image_urls = scrapy.Field()
            #images = scrapy.Field()


            pass

        class ImgData(Item):
            image_urls=scrapy.Field()
            images=scrapy.Field()

    Then we modify the ‘settings.py’. This is required to customize the image pipeline and behavior of spiders. Do not chnage anyother in settings.py file.

        # settings.py in fashionWebScraping folder
        BOT_NAME = 'fashionWebScraping'

        SPIDER_MODULES = ['fashionWebScraping.spiders']
        NEWSPIDER_MODULE = 'fashionWebScraping.spiders'


        # Crawl responsibly by identifying yourself (and your website) on the user-agent
        USER_AGENT = 'Nischay'

        # Obey robots.txt rules
        ROBOTSTXT_OBEY = False

        ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
        IMAGES_STORE = 'PATH of image_scraped folder' 

6. Finally the fun part, time to generate the spider to crawl.

        $ scrapy genspider fashionBOYNER boyner.com

    This command will create 'fashionBOYNER.py' file in spiders folder.

        # fashionBOYNER.py file under fashionWebScraping/spiders

        import scrapy
        from fashionWebScraping.items import FashionwebscrapingItem
        from fashionWebScraping.items import ImgData
        from scrapy.http import Request

        #to read from a csv file
        import csv

        class FashionboynerSpider(scrapy.Spider):
            name = 'fashionBOYNER'
            allowed_domains = ['BOYNER.com']
            start_urls = ['http://BOYNER.com/']

        # This function helps us to scrape the whole content of the website 

            # by following the links in a csv file.
            def start_requests(self):

                # Read main category links from a csv file		
                with open(r"D:\AI and Python\Python\Web_Scraping1\csvFiles\SpiderMainCategoryLinksBOYNER.csv", "rU") as f:
                    reader=csv.DictReader(f)
                
                    for row in reader:

                        url=row['url']
                        # Change the offset value incrementally to navigate through the product list
                        # You can play with the range value according to maximum product quantity
                        link_urls = [url.format(i) for i in range(1,2)]

                        
                        for link_url in link_urls:
                            
                            print(link_url)

                            #Pass the each link containing 100 products, to parse_product_pages function with the gender metadata
                            request=Request(link_url, callback=self.parse_product_pages, meta={'gender': row['gender']})
                
                            yield request

        
            # This function scrapes the page with the help of xpath provided
            def parse_product_pages(self,response):

                item=FashionwebscrapingItem()

                # Get the HTML block where all the products are listed
                # <ul> HTML element with the "products-listing small" class name
                content=response.xpath('//div[starts-with(@class,"product-list-item")]')
                
                # loop through the <li> elements with the "product-item" class name in the content
                for product_content in content:

                    image_urls = []

                    # get the product details and populate the items
                    item['productId']=product_content.xpath('.//a/@data-id').extract_first()
                    item['productName']=product_content.xpath('.//img/@title').extract_first()

                    
                    item['priceSale']=product_content.xpath('.//ins[@class="price-payable"]/text()').extract_first()

                    item['priceOriginal']=product_content.xpath('.//del[@class="price-psfx"]/text()').extract_first()

                    

                    if item['priceOriginal']==None:
                        item['priceOriginal']=item['priceSale']



                    item['imageLink']=product_content.xpath('.//img/@data-original').extract_first()			
                    item['productLink']="https://www.boyner.com.tr"+product_content.xpath('.//a/@href').extract_first()
                    
                    image_urls.append(item['imageLink'])


                    item['company']="BOYNER"
                    item['gender']=response.meta['gender']

                    
                    if item['productId']==None:
                        break

                    yield (item)
                    yield ImgData(image_urls=image_urls)

            def parse(self, response):
                pass

    HTML tags are taken from page source, right click on webpage and select inspect, search **product-list-item**, to get the necessary tags for objects.

7. Generate JSON files from spider.

        $ scrapy crawl -o rawdata_BOYNER.json -t jsonlines fashionBOYNER

    This generates **rawdata_BOYNER.json** in jsonfiles folder. You may have line items with null fields or duplicate values. Both cases require a correction process that I handle with ‘jsonPrep.py’ and **‘deldub.py’**. **‘jsonPrep.py’** looks for the line items with null values and removes them when detected. The result is saved, with a file name starts with ‘prepdata’, into the **‘jsonFiles’** project folder, after null line items are removed. **‘deldub.py’** looks for the duplicate line items and removes them when detected.The result is saved, with a file name starts with **‘finaldata’**, into the **‘jsonFiles’** project folder, after duplicate line items are removed.

        # To remove null values.
        $ python utilityScripts\deldub.py 
        
        # To remove duplicate lines.
        $ python utilityScripts\jsonPrep.py

8. Product data on CSV.

    As we all know the final cleaned data is presented in CSV file format, to convert JSON files to CSV, we use file **'jsontocsv.py'** in ulilityScripts folder.

        # To remove duplicate lines.
        $ python utilityScripts\jsontocsv.py

    Final Product csv file is saved in **final_products_csv** folder.

    ![CSV file](Images_for_blog/Screenshot (117).png) 


Thats it. You can find my github link to all files [here](https://github.com/nischayggowda105/Fashion-We-Scraping).

If you feel this content was useful, go ahead clap for free and follow if you like. 😊








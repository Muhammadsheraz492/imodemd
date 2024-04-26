import csv
import re

import scrapy

class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    # allowed_domains = ["X"]
    # start_urls = ["https://inmodemd.com/find-a-provider"]
    custom_settings = {
        'RETRY_TIMES': 20,
        'HTTPERROR_ALLOW_ALL': True,
        'ROBOTSTXT_OBEY': False,
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_APIKEY': 'your zyte api key',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
        # },
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 20,
        'DOWNLOAD_DELAY': 4,
    }
    def start_requests(self):
        headers = {
            'authority': 'inmodemd.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://inmodemd.com',
            'referer': 'https://inmodemd.com/find-a-provider',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        categories=["139434","23428"]
        searching = [
            "Atlanta GA, USA",
            "Alaska USA",
            "Arizona, USA",
            "Arizona USA",
            "Alabama, USA",
            "Baltimore MD, USA",
            "Boston MA, USA",
            "Chicago, IL, USA",
            "California, USA",
            "Charlotte, NC, USA",
            "Colorado, USA",
            "Charleston, SC, USA",
            "Dallas, TX, USA",
            "Denver, CO, USA",
            "Detroit, MI, USA",
            "Destin, FL, USA",
            "Daytona Beach, FL, USA",
            "El Paso, TX, USA",
            "Estados Unidos",
            "Erie, PA, USA",
            "Eagle Pass, TX, USA",
            "Evansville, IN, USA",
            "Florida, USA",
            "Fort Lauderdale, FL, USA",
            "Fresno, CA, USA",
            "Fort Worth, TX, USA"
            "Bakersfield CA, USA",
            "Birmingham, AL, USA",
            "Birmingham AL, USA"
            , "Atlanta, GA, USA", "San Francisco, CA, USA", "Las Vegas, NV, USA", "Georgia, USA",
            "New York, NY, USA", "North Carolina, USA", "Long Beach, CA, USA", "Fort Lauderdale, FL, USA",
            "Sorrento, FL, USA", "New Jersey, USA", "New Jersey Turnpike, Woodbridge Township, NJ, USA",
            "Calexico, CA, USA",
            "Houston, TX, USA",
            "Hawaii, USA",
            "Hilton Head Island, SC, USA",
            "Huntsville, AL, USA",
            "Honolulu, HI, USA",
            "Indianapolis, IN, USA",
            "Indiana, USA",
            "Illinois, USA",
            "Iowa, USA"
        ]
        with open('data.csv', newline='') as csvfile:
            # Create a CSV reader object that treats the first row as headers
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                # Access columns by header names
                print(row['zip'])
                zipcode = row['zip']
                city = row['city']
                state = row['state']
                form_data = {
                    # 'full_address': search,
                    'full_address': f"{zipcode} {city} {state}",
                    'searchradius': '50',
                    'treatment': '139434',
                    'street_number': '',
                    'street_name': '',
                    'city': 'Golden',
                    'cityNY': '',
                    'postal_code': '',
                    'state_abbr': 'CO',
                    'country': 'United States',
                    # 'lat': '39.755543',
                    # 'lng': '-105.2210997',
                    'physician': '',
                }

                yield scrapy.FormRequest(url='https://inmodemd.com/results/',
                                         headers=headers,
                                         formdata=form_data,
                                         callback=self.parse)



    def parse_address(self,address):
        components = [comp.strip() for comp in address.split(",")]
        street = components[0]
        city_state_zip = components[-2].split()
        city = ""
        state = ""
        zipcode = ""
        if len(city_state_zip) >= 2:
            city = city_state_zip[0]
            state = city_state_zip[1]
            if len(city_state_zip) >= 3:
                zipcode = city_state_zip[2]

        return street, city, state, zipcode

    # Example usage remains the same...

    def parse(self, response):
        print(response.status)
        cards = response.css("div.col-12")

        print(len(cards))
        for card in cards:
            try:
                data = {}
                name = card.css('.dr-name::text').get()
                website = card.css('.dr-website a::attr(href)').get()
                phone = card.css('.dr-phone a::text').get()
                data['name'] = name
                data['website'] = website
                address_element = card.css('div.dr-address::text').getall()
                if len(address_element) >= 1:
                    data['full_adress'] = address_element[-1]
                    data_address = address_element[-1]
                    final_address = data_address.split(",")
                    data['street'] = final_address[0] + ", " + final_address[1]
                    all_data = final_address[-1].split(" ")
                    data['state'] = all_data[1]
                    data['zipcode'] = all_data[2]
                    data['country'] = all_data[3]
                data['phone'] = phone
                yield data
            except Exception as e:
                print("An exception occurred:", e)

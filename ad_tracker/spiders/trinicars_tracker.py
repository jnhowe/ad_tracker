import scrapy
import datetime

from ..items import AdTrackerItem

# type 'scrapy crawl trinicars 2> errors.txt'
class Trini_Cars_Spider(scrapy.Spider):

    name = "trinicars"
    # starting urls that help with defining type of ad
    start_urls = [
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?make_of_car_match=Miscellaneous',
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?license_plate_no_match=Brand%20New', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Motorbike', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Forklift', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?price_details_keyword=Must%20Sell', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?make_of_car_keyword=Rims', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?license_plate_no_match=RORO', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Wagon', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Backhoe', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?price_details_keyword=Quick%20Sale', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?make_of_car_keyword=Parts', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?license_plate_no_match=Unregistered', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Truck', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Tractor', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?price_details_keyword=transfer%20included', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?make_of_car_match=Accessories', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Damaged', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?license_plate_no_match=BOAT', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Bulldozer', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?price_details_keyword=trade%20accepted', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?make_of_car_match=Music', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?main_id_keyword=SOLD', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?model_of_car_keyword=Jet%20Ski', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?make_of_car_match=ATV', 
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?description_of_car_keyword=financing',
        'https://www.trinicarsforsale.com/database/featuredcarsList.php?'
        ]

    def __init__(self):
        self._today = datetime.datetime.today().strftime('%d/%m/%Y')

        self._filename = 'newest_test_trinicars_ad_data.csv'
        

    def parse(self, response):
        ad_links = response.xpath("/html/body/table[5]/tr/td/table/tr/td/a/@href")
        
        # defines type of ad as a standard ad or a specific type; e.g: boat, ATV, etc.
        url = response.url
        if 'https://www.trinicarsforsale.com/database/featuredcarsList.php?page' in url or url == 'https://www.trinicarsforsale.com/database/featuredcarsList.php?' or url == 'https://www.trinicarsforsale.com/database/featuredcarsList.php#topofpage':
            ad_type = 'standard'
        else:
            ad_type = response.url.split('&')[0].split('=')[-1].replace('%', '_')
        
        yield from response.follow_all(ad_links, self.parse_ad, cb_kwargs=dict(ad_type=ad_type))

        # next page logic
        next_page = response.xpath('/html/body/table[6]/tr/td[2]/font[4]/b/a')
        if next_page is not None and next_page != []:
            yield response.follow(next_page[0], callback=self.parse)



    def parse_ad(self, response, ad_type):
        table = response.xpath("/html/body/table[2]/tr/td/table/tr/td[2]/table/tr")
        
        ad_info = {}
        ad_info['id'] = table[0].xpath('.//td[1]/font/b/text()').get()
        ad_info['series'] = table[0].xpath('.//td[2]/font/b/text()').get(default='')
        ad_info['type'] = ad_type
        ad_info['scrape_date(dd/mm/yyyy)'] = self._today

        for row in table[1:]:
            key = row.xpath('.//td[1]/font/b/text()').get()
            if key == None:
                continue
            key = key.strip().rstrip(':').replace(' ', '_').lower()
            value = row.xpath('.//td[2]/font/text() | .//td[2]/font/*/text()').get(default='')

            ad_info[key] = value

        item = AdTrackerItem()

        item['filename'] = self._filename
        item['info'] = ad_info
        yield item
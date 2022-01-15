
import scrapy
import datetime

from ..items import AdTrackerItem

# type 'scrapy crawl pin_tt  2> errors.txt'
class Pin_tt_Spider(scrapy.Spider):

    name = "pin_tt"

    start_urls = ['https://pin.tt/vehicles/cars/',
                    'https://pin.tt/vehicles/vans-trucks/',
                    'https://pin.tt/vehicles/damaged-cars/',
                    'https://pin.tt/vehicles/car-parts/',
                    'https://pin.tt/vehicles/motorbikes/',
                    'https://pin.tt/vehicles/boats/',
                    'https://pin.tt/vehicles/heavy-equipment/',
                    'https://pin.tt/vehicles/tools-equipment/'
                    ]

    def __init__(self):
        '''
        Change filename
        '''
        self._filename = 'testing_pin_tt_ad_data.csv'
        self._today = datetime.datetime.today().strftime('%d/%m/%Y')


    def parse(self, response):
        ad_links = response.xpath('//a[@class="card__title-link "]/@href')
        ad_type = response.url.split('/')[-2]

        yield from response.follow_all(ad_links, self.parse_ad, cb_kwargs=dict(ad_type=ad_type))

        next_page = response.xpath('//*[@class="number-list-next js-page-filter number-list-line"]')
        if next_page is not None and next_page != []:
            yield response.follow(next_page[0], callback=self.parse)
    

    def parse_ad(self, response, ad_type):
        ad_title = response.xpath('//*[@class="title-announcement"]/text()').get().strip()
        ad_id = response.xpath('//span[@class="number-announcement"]/span/text()').get().strip()
        ad_description = response.xpath('//div[@class="announcement-description"]/p/text()').get().strip().encode("ascii", "replace").decode("utf-8")
        date_posted = response.xpath('//*[@class="date-meta"]/text()').get().strip("Posted: ")
        ad_views = int(response.xpath('//*[@class="counter-views"]/text()').get().lstrip("Views: "))
        
        ad_info = {}

        ad_info['title'] = ad_title
        ad_info['scrape_date(dd/mm/yyyy)'] = self._today
        ad_info['type'] = ad_type.encode("ascii", "replace").decode("utf-8")
        ad_info['id'] = ad_id
        ad_info['description'] = ad_description
        ad_info['views'] = ad_views
        ad_info['date_posted'] = date_posted

        ad_details = response.xpath('//ul[@class="chars-column"]/li')

        for detail in ad_details:
            key = detail.xpath('.//span[@class="key-chars"]/text()').get()
            value = detail.xpath('.//*[@class="value-chars"]/text()').get()
            key = key.lower().strip().strip(':').replace(' ', '_')
            value = value.encode("ascii", "replace").decode("utf-8")
            ad_info[key] = value

        item = AdTrackerItem()

        item['filename'] = self._filename
        item['info'] = ad_info
        yield item


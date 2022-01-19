# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import pandas as pd
from scrapy.exceptions import DropItem

class AdTrackerPipeline:

    def __init__(self):
        self._filename = None
        self.all_info = []
        self._today = None
        self.standard_ads = {}


    def open_spider(self, spider):
        print('Starting')

    
    def close_spider(self, spider):
        print('Closing:')
        path = 'c:\\Users\Jafar Howe\Desktop\Projects\cars.tt\\ad_tracker\\' + self._filename
        if not os.path.exists(path):
            print('new', path)
            df = pd.DataFrame(self.all_info)
        else:
            print('old')
            df = pd.read_csv(self._filename)
            df = df.append(self.all_info, ignore_index=True)

        df.to_csv(path, mode='w', index=False, header=True)

        # write date to date file
        dates_file = self._filename[:-4] + '_dates.txt'
        with open(dates_file, 'a') as file:
            file.write('\n'+self._today)        
            
        print(f"Completed webcrawl for {self._today}")
    
    def process_item(self, item, spider):

        # set filename
        if self._filename == None:
            self._filename = item['filename']
            print('filename is', self._filename)

        # set date
        if self._today == None:
            self._today = item['date']
            print('Today\'s date is', self._today)

        info = item['info']

        # removes duplicates only if it is a standard ad, if not, replaces the type of the duplicate
        if info['id'] in self.standard_ads and info['type'] == 'standard':
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            if info['id'] in self.standard_ads:
                self.standard_ads[info['id']]['type'] = info['type']
            else:
                self.standard_ads[info['id']] = info

        self.all_info.append(info)

        return item

import pandas as pd


filename = 'trinicars_ad_data.csv'
today = 'Hello'
dates_file = filename[:-4] + '_dates.txt'
with open(dates_file, 'a') as file:
    file.write('\n'+today)

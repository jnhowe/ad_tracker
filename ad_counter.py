from turtle import done
import pandas as pd
import argparse
import sys


def start(filename, print_ids):
    dates_file = filename[:-4] + '_dates.txt'
    with open(dates_file, 'r') as file:
        first_date = file.readline().strip()
        second_date = file.readline().strip()

        while second_date != '':
            count(filename, first_date, second_date, print_ids)
            second_date = file.readline()


def count(filename, first_date, second_date, print_ids):
    df = pd.read_csv(filename)
    second = df[df['scrape_date(dd/mm/yyyy)'] == second_date]
    first = df[df['scrape_date(dd/mm/yyyy)'] == first_date]

    first_set = set(first['id'].to_list())
    print('New Ads')
    cnt = 0

    for id in second['id'].to_list():
        if id not in first_set:
            if print_ids:
                print(id)
            cnt+=1

    print(f'{cnt} new ads')
    print('='*50)
    second_set = set(second['id'].to_list())
    cnt = 0

    for id in first['id'].to_list():
        if id not in second_set:
            if print_ids:
                print(id)
            cnt+=1

    print(f'{cnt} ads no longer up')    

def main():
    if len(sys.argv) < 2:
        print('Please enter name of csv file')
        exit(1)
    file = sys.argv[1]
    if len(sys.argv) < 3:
        print_ids = False
    else:
        print_ids = sys.argv[2]
    start(file, print_ids)

if __name__ == '__main__':
    main()
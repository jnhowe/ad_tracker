import pandas as pd

path = 'c:\\Users\Jafar Howe\Desktop\Projects\cars.tt\\ad_tracker\\'
old_filename = path + 'pin_tt_ad_data.csv'
new_filename = path + 'testing_pin_tt_ad_data.csv'

old_df = pd.read_csv(old_filename)
new_df = pd.read_csv(new_filename)

# old_df['title'] = old_df['title'].map(lambda name: name[2:-1])
# print(old_df)
# old_df.to_csv(path + 'pin_tt_ad_data.csv', mode='w', index=False, header=True)

final_df = new_df.append(old_df, ignore_index=True)

final_df.to_csv(path + '3' + 'pin_tt_ad_data.csv', mode='w', index=False, header=True)

# def count_diff():
#     filename = ''
#     pd.read_csv(filename)

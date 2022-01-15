import pandas as pd

path = 'c:\\Users\Jafar Howe\Desktop\Projects\cars.tt\\ad_tracker\\'
old_filename = path + 'trinicars_ad_data.csv'
new_filename = path + 'newest_test_trinicars_ad_data.csv'

old_df = pd.read_csv(old_filename)
new_df = pd.read_csv(new_filename)

final_df = new_df.append(old_df, ignore_index=True)

final_df.to_csv(path + '2' + 'testing_trinicars_ad_data.csv', mode='w', index=False, header=True)

# def count_diff():
#     filename = ''
#     pd.read_csv(filename)

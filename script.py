import pandas as pd
import os
import re
from datetime import datetime

# import data
filename = input('Input filename: ')
data = pd.read_csv(filename) 
df = pd.DataFrame(data)

# date needed for filtering the file for upload
date_upload = input('Input date of file upload in this format [M/DD/YYY]: ')

# create a fileformat
match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
date_num = match.group(0)

date_obj = datetime.strptime(date_num, "%Y-%m-%d")
formatted_date = f"{date_obj.month}-{date_obj.day}-{date_obj.year % 100:02}"
formatted_date2 = datetime.strptime(date_num, "%Y-%m-%d").strftime("%m%d%y")

# create folder for the csv files
output_folder = f'FRESH FLOW {formatted_date2}'
os.makedirs(output_folder, exist_ok=True)

# create list of dpd = [36, etc..]
dpd_list = [36, 52, 112, 172, 232]

# select rows depending on the dpd
for dpd in dpd_list:
    filtered_data = df[(df['PARTNERDAYSTHRESHOLD'] == dpd) & (df['HANDOVERDATE'] == date_upload)]

    # add decimal formatting to the column of ob_format
    def format_num(x):
        return f"{x:,.2f}"
    
    filtered_data['ob_format'] = filtered_data['HANDOVERAMOUNT'].apply(format_num)

    data_need = filtered_data[['EMAIL', 'HANDOVERAMOUNT', 'FULLNAME', 'ob_format']]
    data_need.columns = ['Email', '{{ob}}', '{{chname}}', '{{ob_format}}']
     # lagay yung filtered data sa new excel file
    data_need.to_csv(os.path.join(output_folder, f'FRESH FLOW {dpd}DPD {formatted_date}.csv'), index=False)

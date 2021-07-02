'''
    This script  will take all insta picture downloaded  , 
    taking the first picture in each post upload them to html templete and an google sheet file  

'''

#%%
#Grab all the info pic and store them in metadat.json
u = "astro.clo.vn"
p = "tuanyeungan4"
from instaloader import Instaloader 
import instaloader 
insta = Instaloader()
insta.login(u,p)
#%%
! instaloader --l astro.clo.vn -p tuanyeungan4 astro.clo.vn --filename-pattern={date_utc} 
#%%
'''
    Filter post and captions
'''
import os 
import re 
import glob
#Come with globe setting 
img_path= "./astro.clo.vn/*_1.jpg" 
img_paths = [f for f in glob.glob(img_path)]
cap_path= "./astro.clo.vn/*.txt" 
cap_paths = [f for f in glob.glob(cap_path)]

#%% 
'''
This function is useed to open every text file and search for the product name  
'''
product_names = [] 
def product_name_search(file_paths:str): 
    product_name = "Null" 
    with open(file_paths,'r') as file : 
        first_line = file.readline()
        if first_line !="": 
            product_name = first_line
    return product_name                     
for i in cap_paths : 
    name = product_name_search(i)
    product_names.append(name.strip("\n").strip("\n").strip("/"))
print(product_names)
#%%
'''
    Matching caption with timestamp
    Loop through each file_name
'''
from pathlib import Path        

cap_time = set() 
img_time =set() 
for i in cap_paths : 
    path = Path(i).stem
    cap_time.add(path)

for j in img_paths : 
    path2 = Path(j).stem[:-2]
    img_time.add(path)
#The date in cap_time where 
print(img_time[0])
print(cap_time[0])
none = set() 
for i in img_time: 
    if i in cap_time: 
        none.add(i)
print(len(none))
print(none)
#%%
'''
Merge everything in a panda dataframe 
'''
import pandas as pd 
cap_series= pd.Series(product_names,name="Product")
print(cap_series)
img_series= pd.Series(img_paths,name="Img")
print(img_series)
assert cap_series.shape == img_series.shape 
img_df = pd.merge(cap_series,img_series,how="outer",right_index=True,left_index=True)
img_df = img_df.sample(frac=1).reset_index(drop=True)
img_df.tail(20)
# %%
#Display data to html file 
# convert your links to html tags 
from IPython.core.display import display,HTML
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

pd.set_option('display.max_colwidth', None)

image_cols = ['Img' ]  #<- define which columns will be used to convert to html

# Create the dictionariy to be passed as formatters
format_dict = {}
for image_col in image_cols:
    format_dict[image_col] = path_to_image_html
display(HTML(img_df.to_html(escape=False ,formatters=format_dict)))
# %%
img_df.to_html('index.html', escape=False, formatters=format_dict)

'''
    This script  will take all insta picture downloaded  , 
    taking the first picture in each post upload them to html templete and an google sheet file  

'''
#%% 
import pandas as pd 
import os 
import sys 
import glob
from pathlib import Path        
from IPython.core.display import display,HTML
#%% 
'''
    Setting variables and stuff 
'''
username = "" 
pw = "" 
target = "" 

os.environ["username"] = "astro.clo.vn" 
os.environ["pw"] ="tuanyeungan4"  
os.environ["target"] = "astro.clo.vn" 
#%%
'''
    Run this shell if first time runner 
'''
# Use instaloader to download all picture 
! instaloader --l $username  -p $pw --filename-pattern={date_utc} 
#%%
'''
    To update the existed directory 
'''
! instaloader --fast-update --l $username  -p $pw $target --filename-pattern={date_utc} 
#%%
'''
    Filter post and captions to prevent somepost doesn't have caption
    Only post with caption is valid  
'''

def get_path(): 
    cap_path= "./astro.clo.vn/*.txt" 
    #cap_paths = [f for f in glob.glob(cap_path)]
    cap_paths = []
    img_path= "./astro.clo.vn/*_1.jpg" 
    img_paths = []
    none = []
    #Sort the time only add in array if time match  
    for f in glob.glob(img_path):
        c = Path(f).stem[:-2]
        for  i in glob.glob(cap_path): 
            p = Path(i).stem 
            if c ==p :
                img_paths.append(f)
                cap_paths.append(i)
            else : 
                continue 
    return cap_paths, img_paths  
path = get_path()
print(len(path[0]))
print(len(path[1]))

#%% 
'''
This function is useed to open every text file and search for the product name 
on the first line of txt file  
'''
product_names = [] 
def product_name_search(file_paths:str): 
    product_name = "Null" 
    with open(file_paths,'r') as file : 
        first_line = file.readline()
        if first_line !="": 
            product_name = first_line
    return product_name                     
for i in  path[0]: 
    name = product_name_search(i)
    product_names.append(name.strip("\n").strip("\n").strip("/"))
print(product_names)


#%%
'''
Merge everything in a panda dataframe 
'''
cap_series= pd.Series(product_names,name="Product")
print(cap_series)
img_series= pd.Series(path[1],name="Img")
print(img_series)
img_df = pd.merge(cap_series,img_series,how="outer",right_index=True,left_index=True)
img_df = img_df.sample(frac=1).reset_index(drop=True)
img_df.tail(20)
# %%
'''
    Converting the dataframe to html
'''
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
img_df.to_html('./index.html', escape=False, formatters=format_dict)
# %%

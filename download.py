import instaloader
from instaloader import Profile
import sys 
from typing import Optional 

#Get all post from user with provider user name and password , download their own profile 
def download(USER:str,PASSWORD:str,load_session:Optional[bool]=False,update:Optional[bool]=False):
    #Need to set filename pattern here 
    L = instaloader.Instaloader()
    if not update : 
        # Get instance
        # Optionally, login or load session
        L.login(USER, PASSWORD)        # (login)
        #Leave for interactive session 
        #L.interactive_login(USER)      # (ask password on terminal)
                                       #  `instaloader -l USERNAME`
    else : 
        L.load_session_from_file(USER) # (load session created w/

    #Indentify the profile photos            
    profile = Profile.from_username(L.context,[USERNAME])  
    for post in profile.get_posts(): 
        L.download_post(post)


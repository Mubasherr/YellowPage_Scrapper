# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 09:51:42 2023

@author: Developer
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
data=[]

obj={}

what='pizza'
where='new york'
flag= True
FileName=''

target_website = "https://www.yellowpages.com/"+where+"/"+what+"?page1"
countpage=1
while flag:
    print(countpage)
    if(target_website):
        try:
            resp = requests.get(target_website)
            soup=BeautifulSoup(resp.text, 'html.parser')
            allResults = soup.find_all("div",{"class":"result"})
            try:
                dum=soup.find("a",{"class":"next ajax-page"}).get('href')
                # print(type(dum))
                countpage=countpage+1
                target_website = "https://www.yellowpages.com"+str(dum)
            except:
                target_website = None
            for i in range(0,len(allResults)):
                # // for i in range(0,len(allResults)):
                try:
                    obj["name"]=allResults[i].find("a",{"class":"business-name"}).text
                except:
                    obj["name"]=None
                try:
                    obj["phoneNumber"]=allResults[i].find("div",{"class":"phones"}).text
                except:
                    obj["phoneNumber"]=None
                try:
                    obj["address"]=allResults[i].find("div",{"class":"adr"}).text
                except:
                    obj["address"]=None
                try:
                    lateral_string=allResults[i].find("a",{"class":"business-name"}).get('href')
                except:
                    lateral_string=None
                target_website2 = 'https://www.yellowpages.com{}'.format(lateral_string)
                # print(lateral_string)
                resp = requests.get(target_website2).text
                soup=BeautifulSoup(resp, 'html.parser')
                try:
                    obj["Website"]=soup.find("p",{"class":"website"}).find("a").get("href")
                except:
                    obj["Website"]=None
                try:
                    obj["Email"]=soup.find("a",{"class":"email-business"}).get('href').replace("mailto:","")
                except:
                    obj["Email"]=None
                data.append(obj)
                obj={}
                print(data)
        # try:
        #     dum=soup.find("a",{"class":"next ajax-page"}).get('data-page')
        #     print(type(dum))
        #     countpage=countpage+1
        #     target_website = "https://www.yellowpages.com/new-york-ny/restaurants?page"+dum
        # except:
        #     target_website = None
        except:
            if(len(data)!=0):
                df = pd.DataFrame(data)

                # Save the DataFrame to an Excel file
                df.to_excel(FileName+'.xlsx', index=False)
                print("Your file has been saved")
                flag=False
                break
    else:
        df = pd.DataFrame(data)
        # Save the DataFrame to an Excel file
        df.to_excel(FileName+'.xlsx', index=False)
        print("Your file has been saved")
        print("Completed")
        flag=False
        break
                
        
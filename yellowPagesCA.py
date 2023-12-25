
"""
Created on Mon Nov  6 09:51:42 2023

@author: Developer
"""

import requests
from bs4 import BeautifulSoup
import time
data=[]

obj={}

target_website = 'https://www.yellowpages.ca/search/si/1/pizza/Toronto+ON'
countpage=1
while True:
    print(countpage)
    if(target_website):
        resp = requests.get(target_website)
        soup=BeautifulSoup(resp.text, 'html.parser')
        allResults = soup.find("div",{"class":"resultList jsResultsList jsMLRContainer"}).find_all('div',{'class':['listing listing--bottomcta placement  listing--order','listing listing--bottomcta listing--order']})
        time.sleep(3)
        
        try:
            dum_nextsite=soup.find("a",{"class":"ypbtn btn-theme pageButton"}).get('href')
            print((dum_nextsite))
            countpage=countpage+1
            target_website = "https://www.yellowpages.ca"+(dum_nextsite)
        except:
            print("exception Here")
            target_website = None
        for i in range(0,len(allResults)):
            # // for i in range(0,len(allResults)):
            try:
                obj["name"]=allResults[i].find("a",{"class":"listing__name--link listing__link jsListingName"}).text
            except:
                obj["name"]=None
            try:
               # obj["phoneNumber"]=allResults[i].find("div",{"class":"mlr__item__cta jsMlrMenu"}).get("data-phone")
                obj["phoneNumber"] = (allResults[i].find("div",{"class":"listing__mlr__root"}).find("li" ,{"class":"mlr__item mlr__item--more mlr__item--phone jsMapBubblePhone"}).find('li',{'class':"mlr__submenu__item"}).text).strip()
            except:
                obj["phoneNumber"]=None
            try:
                dum = allResults[i].find("div",{"class":"listing__address address mainLocal noNum"}).text
                dum = dum.split("Get directions")
                obj["address"] = dum[0].strip()
               # obj["address"]=allResults[0].find("div",{"class":"listing__address address mainLocal noNum"}).text 
            except:
                obj["address"]=None
                
            # try:
            #     lateral_string=allResults[i].find("a",{"class":"business-name"}).get('href')
            # except:
            #     lateral_string=None
            # target_website2 = 'https://www.yellowpages.com{}'.format(lateral_string)
            # # print(lateral_string)
            # resp = requests.get(target_website2).text
            # soup=BeautifulSoup(resp, 'html.parser')
            try:
                dum = (str(allResults[i].find("div",{"class":"listing__mlr__root"}).find("li" ,{"class":"mlr__item mlr__item--website"})))
                ls = (dum).split("www.")
                ls = ls[1].split(".")
                dum =ls[1].split("%")
               # print(ls[0])
                web = "www."+ls[0]+'.'+dum[0]
                obj["Website"]=web
            except:
                obj["Website"]=None
            # try:
            #     obj["Email"]=soup.find("a",{"class":"email-business"}).get('href').replace("mailto:","")
            # except:
            #     obj["Email"]=None
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
        
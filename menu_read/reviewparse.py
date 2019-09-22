

import pandas as pd
import time as t
from lxml import html
import requests
import json
import numpy as np
from timeit import default_timer as timer
from itertools import cycle
import string
import os
import math
import sys
# In[2]:


os.chdir("/Users/michaelsprintson/Documents/GitHub/me.nu/menu_read/")



food = True

pic_loc = 'ocr/menupictures/pic7.jpg'

pref = "pref_sample.txt"
# In[7]:
def overall(food, pic_loc,pref):

    if food:
        respage = 'https://www.yelp.com/biz/mala-sichuan-bistro-houston-3'
        switch = 'food'
        import ocr_food as ocr
        import just_read_food as jr
        pid = 'ChIJNc4K5cTCQIYRe9OyIN7DcGE'
    else:
        respage = 'https://www.yelp.com/biz/sharetea-houston-2'
        switch = 'tea'
        import ocr_tea as ocr
        import just_read_tea as jr
        pid = 'ChIJjfzjCM_CQIYRPA546CYaE4A'



    # # OCR FUNCTIONALITY TEST

    # In[8]:


    # pip install --upgrade google-cloud-vision


    # In[9]:
    test_file_name = 'final'

    # create dictionary

    ocr.detect_text(pic_loc, test_file_name)


    # In[10]:


    jr.final_dump("ocr/menu_tests/final.txt", pref, True, "final")


    # # IMPORT RESTERAUNT REVIEWS

    # ## IMPORT YELP REVIEWS

    # In[11]:



    reviews_df=pd.DataFrame()

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'
    webpage = ''
    nextpage = 'something'
    xpath_reviews = '//script[@type="application/ld+json"]/text()'
    xpath_nextpage = '//link[@rel="next"]'
    headers = {'User-Agent': user_agent}


    # In[12]:


    if food:
        reviewdf = pd.read_json('menu_parse/bigmala')
    elif not food:
        reviewdf = pd.read_json('menu_parse/sharetea')
    else:
        reviewdf = pd.DataFrame()

        while len(nextpage) > 0:
            #print('1')
            page = requests.get(webpage, headers = headers)#,proxies={"http": proxy, "https": proxy})
            print('pagegot','\r')
            parser = html.fromstring(page.content)
            reviews = parser.xpath(xpath_reviews)
            nextpage = parser.xpath(xpath_nextpage)

            if len(nextpage) > 0:
                nextlink = nextpage[0].get('href')
                print(nextlink, end = '\r')
                webpage = nextlink
                y = json.loads(list(reviews)[0])['review']

                reviewdict = {y.index(i):i for i in y}

                reviewdf = pd.concat([reviewdf,pd.DataFrame(reviewdict).T])

        s = lambda x: list(x.values())[0]
        reviewdf['reviewRating'] = reviewdf['reviewRating'].apply(s)


    # ## IMPORT GOOGLE REVIEWS

    # #### todo: make place id google maps api modular through api call

    # In[13]:


    import googlemaps
    from datetime import datetime


    # In[14]:


    gmapsapikey = json.load(open('menu_parse/gmapsapikey.json', 'r'))[0]


    # In[15]:


    url = f'https://maps.googleapis.com/maps/api/place/details/json?key={gmapsapikey}&place_id={pid}&fields=name,review'
    response = requests.get(url, headers=headers)


    # In[16]:


    googlereviewdict = json.loads(response.content.decode('utf-8'))['result']['reviews']
    googlereviewdict = {googlereviewdict.index(i):i for i in googlereviewdict}

    googlereviewdf = pd.DataFrame(googlereviewdict).T


    # In[17]:


    googlereviewdf = googlereviewdf[['author_name','rating','text']]
    googlereviewdf.columns = ['author','reviewRating','description']
    googlereviewdf


    # In[18]:


    reviewdf = pd.concat([reviewdf,googlereviewdf],sort = False)


    # In[19]:


    reviewdf = reviewdf.reset_index().drop(['index'],axis=1)


    # In[20]:


    #reviewdf['reviewRating'] = reviewdf['reviewRating'].apply(lambda x:x['ratingValue'])
    reviewdf['description'] = reviewdf['description'].apply(lambda x:x.replace('\n','').replace('-',' ').lower())
    reviewdf['description'] = reviewdf['description'].apply(lambda x:' '.join([i for i in x.split(" ") if len(i)>2]))
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    reviewdf['description'] = reviewdf['description'].apply(lambda x:x.translate(translator)).apply(lambda x: ' '.join(x.split()))


    # # GRAB MENU ITEMS

    # In[21]:


    menuitems = json.load(open('menuJSON/final.json'))
    if food:
        menuitems = [x[3:].strip() for x in list(menuitems.keys())]
    menitems = [x.lower() for x in menuitems]


    # ## RANKING MENU ITEMS

    # ### sanity check of menu items

    # In[22]:


    menitems


    # In[23]:


    search = lambda x: [menitem for menitem in menitems if menitem[:math.floor(0.8*len(menitem))] in x]
    reviewdf['containedMenuItems'] = reviewdf['description'].apply(search)


    # In[24]:


    menitemstoreviews = {}
    for menitem in menitems:
        menitemstoreviews[menitem] = [{},list(reviewdf[reviewdf['containedMenuItems'].map(lambda d: menitem in d)].index)]


    # In[25]:


    tot4plusreviews = len(reviewdf[reviewdf['reviewRating'] >= 4])


    # In[26]:


    #total number of 4 plus reviews
    for item in menitemstoreviews:
        #print(item,'------',end = '')
        allratings = []
        fourpluscounter = 0
        twominuscounter = 0
        totalrev = len(menitemstoreviews[item][1])

        for rev in menitemstoreviews[item][1]:
            curstar = reviewdf.iloc[rev]['reviewRating']
            allratings.append(curstar)
            if curstar >= 4:
                fourpluscounter += 1
            elif curstar <= 2:
                twominuscounter += 1
        if not totalrev == 0:
            menitemstoreviews[item][0]['extremerev'] = (fourpluscounter - twominuscounter) / (2 * totalrev)
        else:
            menitemstoreviews[item][0]['extremerev'] = 0
        menitemstoreviews[item][0]['percentageoftotalreviews'] = 8.5 * (fourpluscounter) / tot4plusreviews

        if not len(allratings) == 0:
            menitemstoreviews[item][0]['avgrev'] = sum(allratings)/(5 * len(allratings))
            #print('av rating',sum(allratings)/len(allratings))
        else:
            menitemstoreviews[item][0]['avgrev'] = 0
            #print('no reviews')


    # In[27]:


    itemratings = pd.DataFrame(menitemstoreviews).T
    itemratings.columns = ['ratings','indexes']


    # In[28]:


    itemratings['totalscore'] = itemratings['ratings'].apply(lambda x: sum(x.values()))


    # In[29]:




    allmen = pd.DataFrame(json.load(open('menuJSON/final.json')),index=range(2)).T
    itemratings['price'] = allmen[0].values

    itemratings[['totalscore','price']].sort_values(by = ['totalscore'],ascending = False).to_json('ranking')


overall(food, pic_loc,pref)


# In[ ]:


#
#
#
# # # WIP / TESTING
#
# # In[30]:
#
#
# # itemratings.loc['water boiled beef']['ratings']
#
# # reviewdf[reviewdf['description'].map(lambda d: 'okinawa pearl milk tea' in d)]
#
#
#
# # reviewdf.iloc[548]['description']
#
#
#
# # pd.DataFrame(menitemstoreviews).T
#
# # reviewdf[reviewdf['author']=='Tristan & Ashley Boyd']
#
# # reviewdf.iloc[473]['description']
#
#
#
#
#
#
#
# # #reviewdf.to_json('bigmala')
#
#
# # # USER PREFERENCES
#
# # ## scrape wikipedia for chinese foods (only run once, save results as JSON)
#
# # In[64]:
#
#
# from bs4 import BeautifulSoup
#
#
# # In[65]:
#
#
#
# wikipage = 'https://en.wikipedia.org/wiki/List_of_Chinese_dishes'
# wikipage = requests.get(wikipage).text
# wikidf = pd.DataFrame()
#
# soup = BeautifulSoup(wikipage)
#
# my_tables = soup.findAll('table',{'class':'wikitable'})
#
#
# # In[518]:
#
#
# chinesefoods = []
# for table in my_tables:
#     alla = list(table.findAll('a'))
#     chinesefoods = chinesefoods +[x for x in[alla[i].get('title') for i in range(len(alla))] if type(x) == str]
#
#
# # In[519]:
#
#
# from nltk.corpus import wordnet as wn
# allfoods = list(set([w for s in wn.synset('food.n.02').closure(lambda s:s.hyponyms()) for w in s.lemma_names()])) + chinesefoods
#
#
# # In[520]:
#
#
# len(allfoods)
#
#
# # ## food preferences by users reviews
#
# # In[69]:
#
#
# search = lambda x: [food for food in allfoods if food in x]
#
# #userreviewdf['containedFood='] = userreviewdf['description'].apply(search)
#
#
# # In[ ]:
#
#
#
#
#
# # In[461]:
#
#
# #food = [x.lower() for x in food]
#
#
# # In[ ]:
#
#
#
#
#
# # In[463]:
#
#
# # for i in menuitems:
# #     test = i.split(" ")
# #     test = [x.lower() for x in test]
# #     print(i)
# #     for j in test:
# #         if j in food:
# #             print ('y',j)
# #
#
#
# # # IMPORT USER REVIEWS
#
# # In[34]:
#
#
# def grabfullreviws(ureviews):
#     fullreviews = []
#     curreview = ''
#     for i in range(len(ureviews)):
#         #print('\n')
#         if not (i == len(ureviews)-1):
#             if not type(ureviews[i]) == str:
#                 #print('not a review',ureviews[i],type(ureviews[i]))
#                 pass
#             elif not type(ureviews[i+1]) == str:
#                 #print('middle of a review',ureviews[i],type(ureviews[i]))
#                 curreview = curreview + ureviews[i]
#             elif type(ureviews[i+1]) == str:
#                 #print('end of a review',ureviews[i],type(ureviews[i]))
#                 curreview = curreview + ureviews[i]
#                 fullreviews.append(curreview)
#                 curreview = ''
#         else:
#             curreview = curreview + ureviews[i]
#             fullreviews.append(curreview)
#     return fullreviews
#
#
# # In[35]:
#
#
# unextpage = 'something'
# userpage = 'https://www.yelp.com/user_details_reviews_self?rec_pagestart=0&userid=2fKJeKlPi9le_ta7DPVW_A'
# userreviewdf = pd.DataFrame()
#
# upath_reviews = '//p[@lang="en"]//node()'
# upath_nextpage = '//a[@class="u-decoration-none next pagination-links_anchor"]'
# upath_starrating = '//div[@class="biz-rating__stars"]//div'
#
# while len(unextpage) > 0:
#
#     userpage = requests.get(userpage, headers = headers)#,proxies={"http": proxy, "https": proxy})
#
#     uparser = html.fromstring(userpage.content)
#
#     ureviews = uparser.xpath(upath_reviews)
#
#     unextpage = uparser.xpath(upath_nextpage)
#
#     if len(unextpage) > 0:
#         print(unextpage)
#         userpage = unextpage[0].get('href')
#     ustarratingpath = uparser.xpath(upath_starrating)
#
#     ureviews = [str(i) if not "Element br" in str(i) else 0 for i in ureviews ]
#
#     ufullreviews = grabfullreviws(ureviews)
#
#     fullstars = [i.get('title') for i in ustarratingpath]
#
#     userreviewdf = pd.concat([userreviewdf,pd.DataFrame(list(zip(fullstars,ufullreviews)))])
#
#
# # In[37]:
#
#
# userreviewdf.columns = ['rating','description']
#
#
# # In[38]:
#
#
# userreviewdf.head()
#

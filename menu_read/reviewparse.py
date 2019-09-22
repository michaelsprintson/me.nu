

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
from sklearn import preprocessing
import sys
import googlemaps
from datetime import datetime



#os.chdir("/Users/shjan/Coding/me.nu/")
# os.chdir("/Users/timothygoh/PycharmProjects/me.nu/menu_read/")

# os.chdir("/Users/michaelsprintson/Documents/GitHub/me.nu/menu_read/")


def overall(food, pic_loc,pref):

    #OCR

    if food:
        webpage = 'https://www.yelp.com/biz/mala-sichuan-bistro-houston-3'
        from menu_read import ocr_food as ocr
        from menu_read import just_read_food as jr
        pid = 'ChIJNc4K5cTCQIYRe9OyIN7DcGE'
    else:
        webpage = 'https://www.yelp.com/biz/sharetea-houston-2'
        from menu_read import ocr_tea as ocr
        from menu_read import just_read_tea as jr
        pid = 'ChIJjfzjCM_CQIYRPA546CYaE4A'

    test_file_name = 'final' #name of the file passed between functions 

    ocr.detect_text(pic_loc, test_file_name) #output raw results of ocr and save them to json

    jr.final_dump("menu_read/ocr/menu_tests/final.txt", pref, True, "final")

    reviews_df=pd.DataFrame() #create an empty dataframe to grab reviews from

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'
    nextpage = 'something'
    xpath_reviews = '//script[@type="application/ld+json"]/text()'
    xpath_nextpage = '//link[@rel="next"]'
    headers = {'User-Agent': user_agent} #scraping setup


    if food:
        reviewdf = pd.read_json('menu_read/menu_parse/bigmala')
    elif not food:
        reviewdf = pd.read_json('menu_read/menu_parse/sharetea')
        s = lambda x: list(x.values())[0]
        reviewdf['reviewRating'] = reviewdf['reviewRating'].apply(s)
    else:
        reviewdf = pd.DataFrame() #if no cached results, scrape all reviews

        while len(nextpage) > 0:
            page = requests.get(webpage, headers = headers) #grab the page
            print('pagegot','\r')
            parser = html.fromstring(page.content) #parse page to html
            reviews = parser.xpath(xpath_reviews)
            nextpage = parser.xpath(xpath_nextpage)

            if len(nextpage) > 0: 
                nextlink = nextpage[0].get('href') #grab the next page to scrape if one exists
                print(nextlink, end = '\r')
                webpage = nextlink
                y = json.loads(list(reviews)[0])['review'] #grab all reviews from page

                reviewdict = {y.index(i):i for i in y} #add them to a dictionary

                reviewdf = pd.concat([reviewdf,pd.DataFrame(reviewdict).T]) #add them to dataframe of all reviews

        s = lambda x: list(x.values())[0]
        reviewdf['reviewRating'] = reviewdf['reviewRating'].apply(s) #translate reviewRating into a int
 

    #IMPORT GOOGLE REVIEWS

    gmapsapikey = json.load(open('menu_read/menu_parse/gmapsapikey.json', 'r'))[0]

    url = f'https://maps.googleapis.com/maps/api/place/details/json?key={gmapsapikey}&place_id={pid}&fields=name,review'
    response = requests.get(url, headers=headers)
    
    googlereviewdict = json.loads(response.content.decode('utf-8'))['result']['reviews'] #grab google reviews from API
    googlereviewdict = {googlereviewdict.index(i):i for i in googlereviewdict}

    googlereviewdf = pd.DataFrame(googlereviewdict).T #add google reviews to dataframe
    googlereviewdf = googlereviewdf[['author_name','rating','text']]
    googlereviewdf.columns = ['author','reviewRating','description']

    reviewdf = pd.concat([reviewdf,googlereviewdf],sort = False) #add together google and yelp reviews


    reviewdf = reviewdf.reset_index().drop(['index'],axis=1) 

    #process review text content for food item matching 
    reviewdf['description'] = reviewdf['description'].apply(lambda x:x.replace('\n','').replace('-',' ').lower())
    reviewdf['description'] = reviewdf['description'].apply(lambda x:' '.join([i for i in x.split(" ") if len(i)>2]))
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    reviewdf['description'] = reviewdf['description'].apply(lambda x:x.translate(translator)).apply(lambda x: ' '.join(x.split()))

    # GRAB MENU ITEMS

    menuitems = json.load(open('menu_read/menuJSON/final.json'))
    if food:
        menuitems = [x[3:].strip() for x in list(menuitems.keys())]
    menitems = [x.lower() for x in menuitems]


    search = lambda x: [menitem for menitem in menitems if menitem[:math.floor(0.8*len(menitem))] in x] #search review for menu item
    reviewdf['containedMenuItems'] = reviewdf['description'].apply(search) #keys are reviews and containedMenuItems are the items in each review


    menitemstoreviews = {} #reverse the dataframe -> keys are menu items and values are the reviews that mention it
    for menitem in menitems:
        menitemstoreviews[menitem] = [{},list(reviewdf[reviewdf['containedMenuItems'].map(lambda d: menitem in d)].index)]

 
    def compute(itor,ref): 
        
        #This function takes in a dataframe of menu items to the reviews they appear on, and a dataframe of all reviews.
        #It outputs the sentiment score of each menu item based on the star rating of the reviews the item appears in.
    
        
        tot4plusreviews = len(ref[ref['reviewRating'] >= 4])
        for item in itor: #iterate through menu items, keeping track of the number of reviews over 4 stars and under 2 starts for each menu item
            allratings = []
            fourpluscounter = 0
            twominuscounter = 0
            totalrev = len(itor[item][1])

            for rev in itor[item][1]: #iterate through reviews associated with each menu item
                curstar = ref.iloc[rev]['reviewRating']
                allratings.append(curstar)
                if curstar >= 4:
                    fourpluscounter += 1
                elif curstar <= 2:
                    twominuscounter += 1
            if not totalrev == 0:
                itor[item][0]['extremerev'] = (fourpluscounter - twominuscounter) / (2 * totalrev) #calculate the ratio of extreme ratings
            else:
                itor[item][0]['extremerev'] = 0
            itor[item][0]['percentageoftotalreviews'] = 8.5 * (fourpluscounter) / tot4plusreviews #how many of the total number of 4+ reviews does this item appear in

            if not len(allratings) == 0:
                itor[item][0]['avgrev'] = sum(allratings)/(5 * len(allratings)) #average review
            else:
                itor[item][0]['avgrev'] = 0
                #print('no reviews')
        return itor
    menitemstoreviews = compute(menitemstoreviews,reviewdf)
    itemratings = pd.DataFrame(menitemstoreviews).T #send scores to dataframe for easier analysis
    itemratings.columns = ['ratings','indexes']
    itemratings['totalscore'] = itemratings['ratings'].apply(lambda x: sum(x.values())) #compute total score from yelp and google reviews

    #GRAB A USER'S REVIEWS

    def grabfullreviws(ureviews): 
            # processing function to separate full reviews - for some reason on a user's yelp page
            # each paragraph is processed as a separate element and therefore the scraper thinks it's
            # a new review. This function takes in the unseperated reviews and seperates them fully.
        fullreviews = []
        curreview = ''
        for i in range(len(ureviews)): 
            if not (i == len(ureviews)-1):
                if not type(ureviews[i]) == str:
                    pass
                elif not type(ureviews[i+1]) == str:
                    curreview = curreview + ureviews[i]
                elif type(ureviews[i+1]) == str:
                    curreview = curreview + ureviews[i]
                    fullreviews.append(curreview)
                    curreview = ''
            else:
                curreview = curreview + ureviews[i]
                fullreviews.append(curreview)
        return fullreviews

    userpage = 'https://www.yelp.com/user_details_reviews_self?rec_pagestart=0&userid=2fKJeKlPi9le_ta7DPVW_A'
    
    def userscrape(link): 

        #this functions grab all reviews a user has ever submitted, which will be used to determine how likely the user
        #is to react positively to a menu item. Not commented because its very similar to scraping function above
    
        unextpage = 'something'
        userreviewdf = pd.DataFrame()

        upath_reviews = '//p[@lang="en"]//node()'
        upath_nextpage = '//a[@class="u-decoration-none next pagination-links_anchor"]'
        upath_starrating = '//div[@class="biz-rating__stars"]//div'

        while len(unextpage) > 0:

            userpage = requests.get(userpage, headers = headers)

            uparser = html.fromstring(userpage.content)

            ureviews = uparser.xpath(upath_reviews)

            unextpage = uparser.xpath(upath_nextpage)

            if len(unextpage) > 0:
                print(unextpage)
                userpage = unextpage[0].get('href')
            ustarratingpath = uparser.xpath(upath_starrating)

            ureviews = [str(i) if not "Element br" in str(i) else 0 for i in ureviews ]

            ufullreviews = grabfullreviws(ureviews)

            fullstars = [i.get('title') for i in ustarratingpath]

            userreviewdf = pd.concat([userreviewdf,pd.DataFrame(list(zip(fullstars,ufullreviews)))])
    #userreviewdf = userscrape(userpage)

    userreviewdf = pd.read_json('menu_read/userreviews')

    userreviewdf.columns = ['reviewRating','description'] #formatting of reviews
    userreviewdf['reviewRating'] = userreviewdf['reviewRating'].apply(lambda x: int(x[0:1]))
    reviewdf['description'] = reviewdf['description'].apply(lambda x:x.replace('\n','').replace('-',' ').lower())
    reviewdf['description'] = reviewdf['description'].apply(lambda x:' '.join([i for i in x.split(" ") if len(i)>2]))
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    reviewdf['description'] = reviewdf['description'].apply(lambda x:x.translate(translator)).apply(lambda x: ' '.join(x.split()))


    #scrape common chinese foods from wikipedia to help with recognizing common foods in our user's reviews

    from bs4 import BeautifulSoup

    wikipage = 'https://en.wikipedia.org/wiki/List_of_Chinese_dishes'
    wikipage = requests.get(wikipage).text
    wikidf = pd.DataFrame()

    soup = BeautifulSoup(wikipage,features="lxml")

    my_tables = soup.findAll('table',{'class':'wikitable'})


    chinesefoods = []
    for table in my_tables:
        alla = list(table.findAll('a'))
        chinesefoods = chinesefoods +[x for x in[alla[i].get('title') for i in range(len(alla))] if type(x) == str]

    with open('menu_read/allfoods.json') as f:
        allfoods = json.load(f)


    # find foods in user's reviews and use that to determine which of the menu items is more appealing to that user

    search = lambda x: [food for food in allfoods if food in x]

    userreviewdf['containedFood'] = userreviewdf['description'].apply(search) #search user's reviews for food items

    foodtoreviewunfiltered = {} #map all food items to reviews that contain that item
    for food in allfoods:
        foodtoreviewunfiltered[food] = [{},list(userreviewdf[userreviewdf['containedFood'].map(lambda d: food in d)].index)]

    foodtoreview = {k:v for (k,v) in foodtoreviewunfiltered.items() if not len(v[1]) == 0} #dictionary of all non zero results

    userrevscores = compute(foodtoreview,userreviewdf) #use compute function from earlier to compute scores

    userratings = pd.DataFrame(userrevscores).T #formatting
    userratings.columns = ['ratings','indexes']
    userratings['totalscore'] = userratings['ratings'].apply(lambda x: sum(x.values()))
    userratings['totalscore'].sort_values(ascending = False).head()

    for i in list(itemratings.index): #edit total score of a menu item by updating it with a scaled version of the user's ratings for 
                                      #foods that that menu item contains.
        test = i.split(" ")
        test = [x.lower() for x in test]
        for j in test:
            if j in allfoods:
                itemratings.at[i,'totalscore'] = itemratings.loc[i]['totalscore'] + 0.3 * userratings['totalscore'][test.index(j)]    #             print ('after',itemratings.at[i,'totalscore'])

    allmen = pd.DataFrame(json.load(open('menu_read/menuJSON/final.json')),index=range(2)).T
    itemratings['price'] = allmen[0].values

    min_max_scaler = preprocessing.MinMaxScaler() 
    x = itemratings[['totalscore']].values.astype(float) #processing to scale scores between 0 and 10 for a ranking system
    itemrating_scaled = min_max_scaler.fit_transform(x)
    itemratings['totalscore'] = [math.ceil(10* x[0]) for x in itemrating_scaled]
    itemratings[['totalscore','price']].sort_values(by = ['totalscore'],ascending = False).T.to_json('menu_read/ranking.json') #send results to JSON

def run():
    food = True

    #pic_loc = 'ocr/menupictures/othermenu/teamenu.jpg'
    pic_loc = 'menu_read/ocr/menupictures/pic7.jpg'

    pref = 'menu_read/preferencesData.json'

    overall(food, pic_loc, pref)



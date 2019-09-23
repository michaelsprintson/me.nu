# *Me.nu*

*Me.nu is a web application optimized for mobile platforms that creates individually-tailored menus. It uses
 Yelp, Google Reviews, and user-specific preferences to determine the perfect recommendations for me n you.* 
 
 Me.nu won first place overall at HackRice 9! [(presentation and demo link)](https://docs.google.com/presentation/d/1TuNCihdM04-Vg7iJvhlEi2cJuIjqjIYcAnWkSz_xGfo/edit?usp=sharing)
 
## Features
* Uses Google Vision API's Optical Character Recognition to parse a menu
* Filters results based on user preferences (budget, dietary. restrictions, etc)
* Collects reviews from multiple services, including Google Reviews and Yelp, to create an accurate prediction of the best dishes at a resteraunt.
* Factors in a user's previous Yelp reviews to help predict which menu items would be most appealing to them
* Creates a personalized account tied to a user's Yelp account to help learn a user's preferenences.
* Pulls food items from online libraries and dictionaries to give a full featured prediction of a user's tastes.
* Uses simplified relational calculus to calculate a score for each individual menu item.

## Menu Item Rating Algorithm 
We wrote this algorithm for our program to rate each dish from the menu input. It factors in the average rating, a correction factor for other reviewers' perceptions of the dish as positive or negative, as well as the tendency of better items to typically have more reviews overall. 
![Menu Item Rating Algorithm](https://github.com/michaelsprintson/me.nu/blob/master/hr9%20equation.PNG)

## How to run
1. Setup [Google Cloud Vision API](https://cloud.google.com/vision/docs/before-you-begin) for your project to enable optical character recognition (OCR) for menu scanning.
    1a. put the Google Vision Service Account Key in a file called <code>apikey.json</code> inside of the <code>menu_read</code> directory 
2. Setup [Google Cloud Maps Places API](https://developers.google.com/places/web-service/intro) to enable google review scraping
   2a. *please put the Google Maps API key in a file called <code>gmapsapikey.json</code> inside of the <code>menu_parse</code> directory
3. Install neccesary dependencies with ```pip install -r requirements.txt```
4. Start the server with ```python3 app.py```

## Team
Me.nu was created by Timothy Goh (tGoh98), Michael Sprintson (michaelsprintson), Seung Hun Jang (sj43), and Colin King (colinbking) for HackRice9. Read more about it in the [Devpost](https://devpost.com/software/me-nu). Presentation slides can be found [here](https://docs.google.com/presentation/d/1TuNCihdM04-Vg7iJvhlEi2cJuIjqjIYcAnWkSz_xGfo/edit?usp=sharing).

![Me.nu Logo](https://github.com/michaelsprintson/me.nu/blob/tim/menu_read/static/images/menuLogo.png)

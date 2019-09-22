# *Me.nu*

*Me.nu is a web application optimized for mobile platforms that creates individually-tailored menus. It uses
 Yelp, Google Reviews, and user-specific preferences to determine the perfect recommendations for me n you.* 

## Features

Uses Google Vision API's Optical Character Recognition to parse a menu
Filters results based on user preferences (budget, dietary. restrictions, etc)
Collects reviews from multiple services, including Google Reviews and Yelp, to create an accurate prediction of the best dishes at a resteraunt.
Factors in a user's previous Yelp reviews to help predict which menu items would be most appealing to them
Creates a personalized account tied to a user's Yelp account to help learn a user's preferenences.
Pulls food items from online libraries and dictionaries to give a full featured prediction of a user's tastes.
Uses simplified relational calculus to calculate a score for each individual menu item.

## How to run

Setup Google Cloud Vision API for your project to enable optical character recognition (OCR) for menu scanning. 1a. put the Google Vision Service Account Key in a file called apikey.json inside of the menu_read directory
Setup Google Cloud Maps Places API to enable google review scraping 2a. *please put the Google Maps API key in a file called gmapsapikey.json inside of the menu_parse directory
Install Xpath to enable extraction of yelp reviews
Install dependencies with pip install -r requirement.txt
Start the server with flask run

## Menu Item Rating Algorithm 

We wrote this algorithm for our program to rate each dish from the menu input. It factors in the average rating, a correction factor for other reviewers' perceptions of the dish as positive or negative, as well as the tendency of better items to typically have more reviews overall. 
![Menu Item Rating Algorithm](https://github.com/michaelsprintson/me.nu/blob/master/hr9%20equation.PNG)

## Team
Me.nu was created by Timothy Goh (tGoh98), Michael Sprintson (michaelsprintson), Seung Hun Jang (sj43), and Colin King (colinbking) for HackRice9. Read more about it in the [Devpost](https://devpost.com/software/me-nu).

![Me.nu Logo](https://github.com/michaelsprintson/me.nu/blob/tim/menu_read/static/images/menuLogo.png)

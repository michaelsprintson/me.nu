# *Me.nu*

*Me.nu is a web application optimized for mobile platforms that creates individually-tailored menus. It uses
 Yelp, Google Reviews, and user-specific preferences to determine the perfect recommendations for me n you.* 

## How to run
1. Setup [Google Cloud Vision API](https://cloud.google.com/vision/docs/before-you-begin) for your project to enable optical character recognition (OCR) for menu scanning.
    1a. put the Google Vision Service Account Key in a file called <code>apikey.json</code> inside of the <code>menu_read</code> directory 
2. Setup [Google Cloud Maps Places API](https://developers.google.com/places/web-service/intro) to enable google review scraping
   2a. *please put the Google Maps API key in a file called <code>gmapsapikey.json</code> inside of the <code>menu_parse</code> directory
3. Install [Xpath](https://docs.scrapy.org/en/xpath-tutorial/topics/xpath-tutorial.html) to enable extraction of yelp reviews
4. Install dependencies with ```pip install -r requirement.txt```
5. Start the server with ```flask run```

## Team
Me.nu was created by Timothy Goh (tGoh98), Michael Sprintson (michaelsprintson), Seung Hun Jang (sj43), and Colin King (colinbking) for HackRice9. Read more about it in the [Devpost](https://devpost.com/software/me-nu).

![Me.nu Logo](https://github.com/michaelsprintson/me.nu/blob/tim/menu_read/static/images/menuLogo.png)

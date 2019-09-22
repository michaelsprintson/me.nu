# *Me.nu*

*Me.nu is a web application optimized for mobile platforms that recommends users what to order at restaurants. It uses
 yelp, google reviews, and user-specific preferences to create the optimal order.* 

## Setup 
1. Setup [Google Cloud Vision API](https://cloud.google.com/vision/docs/before-you-begin) for your project to enable optical character recognition (OCR) for menu scanning.
    1a. put the Google Vision Service Account Key in a file called <code>apikey.json</code> inside of the <code>menu_read</code> directory 
2. Setup [Google Cloud Maps Places API](https://developers.google.com/places/web-service/intro) to enable google review scraping
    2a. *please put the Google Maps API key in a file called <code>gmapsapikey.json</code> inside of the <code>menu_parse</code> directory
3. Install [Xpath](https://docs.scrapy.org/en/xpath-tutorial/topics/xpath-tutorial.html) to enable extraction of yelp reviews
4. Install pandas, requests, lxml, Flask, and other necessary packages on the project interpreter if using an IDE, 
or install dependencies with <code>npm install</code>.

### How to run
Please download [Python 3.7+](https://www.python.org/downloads/)

run app.py
* \*please make sure the picture you take of the menu is clear for OCR to work optimally*

*yeat*

## Team
* Me.nu was made by Timothy Goh, Michael Sprintson, Seung Hun Jang, and Colin King


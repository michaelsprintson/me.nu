import os
import io
from collections import defaultdict
import json
import re
#from google.cloud import vision

# set environment variable for google api credential
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\shjan\Downloads\ocrtest1-bf8fefb197a6.json"


"""
This file reads menu OCR results from myfile.txt and dumps json dictionary of menu item to price
"""




def load_words():
    with open(r"ocr\words_alpha.txt") as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def detect_text(path, savepath):
    """Detects text in the file."""

    file1 = io.open("ocr\\menu_tests\\" + savepath +
                    ".txt", "w", encoding="utf-8")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts[0].description.split('\n'):
        text_lst = re.sub("([^\x82\x00-\x7F])+", " ", text).split()

        first_word = text_lst[0] if text_lst else ''
        if first_word and not first_word[-1].isdigit():
            first_word = first_word[:-1]

        file1.writelines(first_word + ' ' + ' '.join(
            [word for word in text_lst[1:] if (len(word) > 2 and word.lower() in d)]) + '\n')

    file1.close()



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def findprice(usemenu):
    price_list = []
    for lineidx in range(len(usemenu)):
        if is_number(usemenu[lineidx]):
            price_list.append(float(usemenu[lineidx].strip()))
    return price_list


def findfood(usemenu):
    food_list = []
    for lineidx in range(len(usemenu)):
        if not is_number(usemenu[lineidx]):
            food_list.append(usemenu[lineidx].strip())
    return food_list


def findidx(usemenu, findprice):
    """
    :param usemenu: menu result from OCR
    :param findprice: True if we are finding the price section idx, otherwise for food section idx
    :return:
    """

    for lineidx in range(len(usemenu)):
        if findprice:
            if (usemenu[lineidx][0]).isdigit():  # if its a price
                sectionidx = lineidx
                break
        else:  # if its a food item
            if not (usemenu[lineidx][0]).isdigit():
                sectionidx = lineidx
                break
        if lineidx == len(usemenu) - 1:
            return len(usemenu) - 1
    return sectionidx


def recallfind(usemenu):
    """
    :param usemenu: menu result of OCR
    :return: a list of the indexes in the menu lines where it changes from dishes to itesm
    """
    current = 0
    outto = [0]
    pricefind = True
    while current < len(usemenu)-1:
        sectionplace = findidx(usemenu[current:], pricefind)
        current += sectionplace
        outto.append(current)
        pricefind = not pricefind
    print(outto)
    return outto


def first_clean(ocr_menu):
    menu = io.open(ocr_menu, "r", encoding="utf-8")
    menu_lines = menu.readlines()

    remove_bad = []  # empty list to hold raw lines of the cleaned up full menu

    # get rid of the random numbers from OCR and the menu headings
    for lineidx in range(len(menu_lines)):
        item = menu_lines[lineidx].strip()
        if (len(item) >= 4) and (item[3].isdigit() or ((not item[0].isdigit() and item[1].isdigit()))):
            remove_bad.append(menu_lines[lineidx])

    return remove_bad


def make_fooddict(foods, prices):
    menu_dict = defaultdict()
    for foodidx in range(len((foods))):
        menu_dict[foods[foodidx]] = prices[foodidx]
    return menu_dict


def filter(menu_dict, user_pref):
    pref = open(user_pref, "r")  # load user preferences txt
    pref_lines = pref.readlines()
    budget = float(pref_lines[0].strip())
    # budget = 100.0
    eats_meat = bool(pref_lines[1].strip())
    user_likes = (pref_lines[2].strip().split())

    # filters out dishes based on vegetarian status and budget
    meats = {"Beef", "Pork", "Duck", "Chicken", "Lamb", "Blood", "Lung",
             "Meat", "Fish", "Clam", "Tripe", "Prawn", "Rib", "Tilapia"}
    newdict = {}
    for dish in menu_dict:
        item = menu_dict[dish]
        if menu_dict[dish] <= budget:
            if not eats_meat:
                for meat in meats:
                    if meat in dish:
                        nomeat = False
                if nomeat:
                    newdict[dish] = menu_dict[dish]
            else:
                newdict[dish] = menu_dict[dish]
    return newdict


def final_dump(menu, pref, dump, dumpsavename):
    """
    :param menu: OCR result of menu as txt
    :param pref: preferences input as txt
    :param dump: True if you want to dump menudict result to json
    :return:
    """
    cleaned = first_clean(menu)
    foods = findfood(cleaned)
    prices = findprice(cleaned)
    menudict = make_fooddict(foods, prices)
    menudict = filter(menudict, pref)
    if dump:
        with open("menu_read\\menuJSON\\" + dumpsavename + '.json', 'w') as cleaned_menu:
            json.dump(menudict, cleaned_menu)
    return menudict




print (final_dump(r"ocr\menu_tests\weirdfiletest18.txt", "menu_read\pref_sample.txt", False, "as"))
# create dictionary
d = load_words()

pref_location = "menu_read\\pref_sample.txt"

# # run test with normal pictures
# pic_loc = 'ocr\\menupictures\\othermenu\\othermenu7.jpg'
# test_file_name = 'othermenutest7'
# detect_text(pic_loc, test_file_name)
# print(final_dump('ocr\\menu_tests\\' + test_file_name + '.txt', pref_location, True, test_file_name))

# run test with weird pictures

# for i in range(2, 5):
#     pic_loc = 'ocr\menupictures\weirdpic\wpic' + str(i) + '.jpg'
#     file_name = 'weirdfiletest' + str(i)
#     detect_text(pic_loc, file_name)
#     print(final_dump("ocr\menu_tests\weirdfiletest" + str(i) + ".txt",
#                      pref_location, True, "weirdpic" + str(i)))

import os
import io
from collections import defaultdict
import json
import re


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
    #print(remove_bad)
    return remove_bad


def make_fooddict(foods, prices):
    menu_dict = defaultdict()
    #print (len(foods), len(prices))
    for foodidx in range(len(foods)):
        #print(foods[foodidx], prices[foodidx])
        menu_dict[foods[foodidx]] = prices[foodidx]
    return menu_dict


def filter(menu_dict, user_pref):
    pref = json.load(open(user_pref, "r"))

    budget = float(pref['budget'].strip())
    # budget = 100.0

    eats_meat = not pref['diet-veg'] in ['True']
    takeout_pref = (pref['diet-exclude'].strip().split(','))

    # filters out dishes based on vegetarian status and budget
    meats = ["Beef", "Pork", "Duck", "Chicken", "Lamb", "Blood", "Lung",
             "Meat", "Fish", "Clam", "Tripe", "Prawn", "Rib", "Tilapia", "Rabbit", "Bacon"]

    newdict = {}
    meatcontentbool = {dish:False for dish in menu_dict}
    for dish in menu_dict:
        if menu_dict[dish] <= budget:
            if not eats_meat:
                for meat in meats:
                    if meat in dish:
                        meatcontentbool[dish] = True
            else:
                newdict[dish] = menu_dict[dish]
    if not eats_meat:
        kept = [dish for (dish,boool) in meatcontentbool.items() if boool == False]
        for keptmeal in kept:
            newdict[keptmeal] = menu_dict[keptmeal]

    finaldict= {} # filter out dishes specified as bad by user
    for dish in newdict:
        badstuffin = False
        for takeout in takeout_pref:
            if takeout.lower() in dish.lower():
                badstuffin = True
        if not badstuffin:
            finaldict[dish] = newdict[dish]

    return finaldict


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
        with open("menu_read/menuJSON/" + dumpsavename + '.json', 'w') as cleaned_menu:
            json.dump(menudict, cleaned_menu)
    return menudict





# create dictionary
#d = load_words()

# run test with normal pictures

# detect_text('ocr\menupictures\pic6.jpg', 'pic6test')


# run test with weird pictures

# for i in range(2, 5):
#     pic_loc = 'ocr\menupictures\weirdpic\wpic' + str(i) + '.jpg'
#     weird_file_name = 'weirdfiletest' + str(i)
#     detect_text(pic_loc, weird_file_name)
print(final_dump("menu_read/ocr/menu_tests/final.txt",
                      "menu_read/preferencesData.json", False, "weirdpic"))

import os
import io
from collections import defaultdict
import json

"""
This file reads menu OCR results from myfile.txt and dumps json dictionary of menu item to price
"""



#print(os.getcwd())
pref = open("menu_read\pref_sample.txt", "r") #load user preferences txt
pref_lines = pref.readlines()
#budget = float(pref_lines[0].strip())
budget = 100.0
eats_meat = bool(pref_lines[1].strip())
user_likes = (pref_lines[2].strip().split())


#menu = io.open("ocr\myfile.txt", "r", encoding="utf-8")
#menu = io.open("ocr\menu_tests\soups.txt", "r", encoding="utf-8")
#menu = io.open("ocr\menu_tests\weirdapps.txt", "r", encoding="utf-8")
menu = io.open("ocr\menu_tests\pic4test.txt", "r", encoding="utf-8")
#menu = io.open("ocr\menu_tests\pic7test.txt", "r", encoding="utf-8")



menu_lines = menu.readlines()
# print(len(menu_lines)), 'l'

remove_bad = [] # empty list to hold raw lines of the cleaned up full menu

# get rid of the random numbers from OCR and the menu headings
for lineidx in range(len(menu_lines)):
    # print (lineidx, menu_lines[lineidx])
    item = menu_lines[lineidx].strip()
    if (len(item) >= 4) and (item[3].isdigit() or ((not item[0].isdigit() and item[1].isdigit()))):
        #((len(item) > 4) and not (len(item) > 1 and not item[0].isdigit() and not item[1].isdigit())):
        #print(item, 'added')
        remove_bad.append(menu_lines[lineidx])

print((remove_bad), 'num lines in removed')
# getting the end index for each section of the menu
# each section is a section of the dishes, or the prices of the dishes

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
        if lineidx == len(usemenu)- 1:
            return len(usemenu)- 1
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
        sectionplace = findidx(remove_bad[current:], pricefind)
        current += sectionplace
        outto.append(current)
        print (remove_bad[current], current, 'the current')
        pricefind = not pricefind
    return outto

section_idx_list = recallfind(remove_bad)
# print (section_idx_list)


sections = [] #list of lists, sublists are menu item sections, following list is corresponding price section
for i in range(len(section_idx_list)-1):
    subsection = remove_bad[section_idx_list[i] : section_idx_list[i+1]+1] #holds one section of prices or items

    #print (len(subsection), subsection)
    sections.append(subsection)

# print ("_________SECTIONS________")
# print (len(sections))
#


menu_dict = defaultdict()
for sectionidx in range(0,len(sections),2): #grab each section of items
    for itemidx in range(len(sections[sectionidx])): #grab each menu item
        #print (sections[sectionidx][itemidx], sections[sectionidx+1][itemidx])
        if itemidx == len(sections[sectionidx])-1:
            break
        #print (sections[sectionidx][itemidx], 'itemidx problem',itemidx, sections[sectionidx+1][itemidx])
        menu_dict[sections[sectionidx][itemidx].strip()] = float(sections[sectionidx+1][itemidx].strip())


# print(len(menu_dict))


# filters out dishes based on vegetarian status and budget
meats = {"Beef", "Pork", "Duck", "Chicken", "Lamb", "Blood", "Lung", "Meat", "Fish", "Clam", "Tripe", "Prawn", "Rib", "Tilapia"}
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

#
# print (newdict)

# print ("_______________________")
# print (newdict)
# print (len(newdict))


with open('first_page_cleaned_menu_dict.json', 'w') as cleaned_menu:
    json.dump(newdict, cleaned_menu)

# #
